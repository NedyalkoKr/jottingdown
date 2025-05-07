import re
from urllib.parse import urlencode
from django.template.loader import render_to_string
from difflib import SequenceMatcher
from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.db.models import Func, F, Q, Value, CharField, FloatField, Count, TextField, Max, Sum
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank, SearchHeadline, TrigramSimilarity, TrigramWordSimilarity
from core.models import Community
from topics.models import Topic
from search.models import SearchHistory, SavedSearch
from .forms import NewSavedSearchFromKeywordModelForm, NewSavedSearchModelForm


STOP_WORDS = {
  "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has", "he",
  "in", "is", "it", "its", "of", "on", "that", "the", "to", "was", "were", "will", "with"
}

def remove_stop_words(query):
  words = query.lower().split()
  filtered_words = [word for word in words if word not in STOP_WORDS]
  return " ".join(filtered_words) if filtered_words else query


def highlight_text(text, query, min_length=3):
  query_words = query.split()
  if not query_words:
    return text

  highlighted_text = text
  pattern = r'\w+'
  words = [(m.start(), m.end(), m.group()) for m in re.finditer(pattern, text, re.IGNORECASE)]

  for q_word in query_words:
    if len(q_word) < min_length:
      continue
    # Dynamic threshold based on query length
    query_length = len(q_word)
    similarity_threshold = 0.2 if query_length < 5 else 0.3 if query_length <= 10 else 0.4

    matches = []
    for start, end, word in words:
      similarity = SequenceMatcher(None, q_word.lower(), word.lower()).ratio()
      if similarity >= similarity_threshold and len(word) >= min_length:
        matches.append((start, end, word))

    matches.sort(key=lambda x: x[0], reverse=True)
    for start, end, match in matches:
      highlighted_text = (
        highlighted_text[:start] +
        f'<span style="background-color: #FFFBC8;">{highlighted_text[start:end]}</span>' +
        highlighted_text[end:]
      )
    return highlighted_text


class SearchCommunityTopicsView(LoginRequiredMixin, ListView):

  http_method_names = ['get']
  context_object_name = "topics"
  template_name = "search/search_community_topics.html"

  def get_queryset(self):
    query = self.request.GET.get("q", "").strip()
    if not query:
      return Topic.objects.none()
    cleaned_query = remove_stop_words(query)
    search_vector_fields = SearchVector("content", "title", config='english')
    search_query = SearchQuery(cleaned_query, search_type="websearch",)
    search_content_headline = SearchHeadline(
      "content",
      search_query,
      start_sel='<span style="background-color: #FFFBC8;">',
      stop_sel='</span>', 
      highlight_all=True,
    )
    search_title_headline = SearchHeadline(
      "title",
      search_query,
      start_sel='<span style="background-color: #FFFBC8;">',
      stop_sel='</span>', 
      highlight_all=True,
    )
    topics = Topic.objects.annotate(
      search=search_vector_fields,
      rank=SearchRank(search_vector_fields, search_query, cover_density=True), search_content_highlight=search_content_headline, search_title_highlight=search_title_headline).filter(search_vector=search_query).filter(community=Community.objects.get(slug=self.kwargs['slug'])).order_by("-rank")
    
    if not topics.exists():
      query_length = len(query.replace(" ", ""))
      if query_length < 5:
        # More lenient for short queries
        trigram_threshold = 0.2 
      elif query_length <= 10:
        trigram_threshold = 0.3
      else:
        # Stricter for long queries
        trigram_threshold = 0.4
      
      topics = Topic.objects.annotate(similarity=TrigramSimilarity('content', query) + TrigramSimilarity('title', query)
      ).filter(community=Community.objects.get(slug=self.kwargs['slug'])).filter(
        Q(similarity__gt=trigram_threshold) & Q(user=self.request.user)
      ).order_by("-similarity")

      for topic in topics:
        topic.search_content_highlight = highlight_text(topic.content, query)
        topic.search_title_highlight = highlight_text(topic.title, query)
      return topics
    return topics

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context["search_query"] = self.request.GET.get("q")
    context['search_count'] = self.get_queryset().count()
    context['community'] = Community.objects.get(slug=self.kwargs['slug'])
    return context


class SearchAllTopicsView(LoginRequiredMixin, ListView):

  http_method_names = ['get']
  context_object_name = "topics"
  template_name = "search/search_all_topics.html"

  # def update_search_history(self, cleaned_query):
  #   """Update or create search history entry for the given query."""
  #   obj, created = SearchHistory.objects.get_or_create(query=cleaned_query)
  #   if not created:
  #     obj.search_count = F('search_count') + 1
  #     obj.save(update_fields=['search_count'])
  #   else:
  #     obj.search_count = 1
  #     obj.save(update_fields=['search_count'])

  def update_search_history(self, cleaned_query):
    """Update or create search history entry for the given query, only for new user queries."""
    user = self.request.user
    try:
      # Try to get existing search history for this user and query
      obj = SearchHistory.objects.get(user=user, query=cleaned_query)
      # If it exists, do not increment search_count (already counted for this user)
    except SearchHistory.DoesNotExist:
      # If it doesn't exist, create a new entry with search_count=1
      obj = SearchHistory.objects.create(
        user=user,
        query=cleaned_query,
        search_count=1
      )

  def get_full_text_search_queryset(self, cleaned_query):
    search_vector_fields = SearchVector("content", "title", config='english')
    search_query = SearchQuery(cleaned_query, search_type="websearch")
    search_content_headline = SearchHeadline(
      "content",
      search_query,
      start_sel='<span style="background-color: #FFFBC8;">',
      stop_sel='</span>',
      highlight_all=True,
    )
    search_title_headline = SearchHeadline(
      "title",
      search_query,
      start_sel='<span style="background-color: #FFFBC8;">',
      stop_sel='</span>',
      highlight_all=True,
    )
    topics = Topic.objects.annotate(
      search=search_vector_fields,
      rank=SearchRank(search_vector_fields, search_query, cover_density=True),
      search_content_highlight=search_content_headline,
      search_title_highlight=search_title_headline,
    ).filter(
      search_vector=search_query
    ).prefetch_related(
      'user', 'community',
    ).exclude(
      user=self.request.user
    ).order_by(
      "-rank", "-created"
    )
    return topics
  
  def get_trigram_search_queryset(self, query, query_length):
    cleaned_query = remove_stop_words(query)
    if query_length < 5:
      trigram_threshold = 0.2
    elif query_length <= 10:
      trigram_threshold = 0.3
    else:
      trigram_threshold = 0.4
    topics = Topic.objects.annotate(
      similarity=TrigramSimilarity('content', query) + TrigramSimilarity('title', query)
    ).filter(
      Q(similarity__gt=trigram_threshold)
    ).exclude(
      user=self.request.user
    ).order_by(
      "-similarity"
    )
    for topic in topics:
      topic.content_highlight = highlight_text(topic.content, cleaned_query)
      topic.search_title_highlight = highlight_text(topic.title, cleaned_query)
    return topics

  def get_queryset(self):
    query = self.request.GET.get("sq", "").strip()
    cleaned_query = remove_stop_words(query)
    topics = Topic.objects.none()
    if query:
      topics = self.get_full_text_search_queryset(cleaned_query)
      if not topics.exists():
        query_length = len(query.replace(" ", ""))
        topics = self.get_trigram_search_queryset(query, query_length)
      # Only update search history if there are results
      if topics.exists():
        self.update_search_history(cleaned_query)
    return topics
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    query = self.request.GET.get("sq", "").strip()
    search_history_agg = SearchHistory.objects.values('query').annotate(
      total_count=Sum('search_count')
    ).order_by('-total_count')
    context["search_query"] = query
    context['search_history_agg'] = search_history_agg
    context['search_count'] = self.get_queryset().count()
    return context


class SearchesView(LoginRequiredMixin, ListView):
  
  http_method_names = ['get']
  context_object_name = "searches"
  template_name = "search/searches.html"

  def get_queryset(self):
    return SearchHistory.objects.values('query').annotate(
      total_count=Sum('search_count')
    ).order_by('-total_count')
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    return context


class NewSavedSearchView(LoginRequiredMixin, CreateView):

  model = SavedSearch
  form_class = NewSavedSearchModelForm
  http_method_names = ["get", "post",]
  # permission_required = ('accounts.full_access_to_entire_platform',)
  template_name = "search/search_posts.html"
  
  def form_valid(self, form):
    instance = form.save(commit=False)
    search_query = self.kwargs['search_query']
    form.instance.name = search_query
    form.instance.user = self.request.user
    # if search_query is not None:
    #   query_words = search_query.split('+')
    #   form.instance.name = query_words
    #   form.instance.user = self.request.user
    form.save()
    return HttpResponseRedirect(self.get_success_url())

  def get_success_url(self, **kwargs):
    query = self.kwargs['search_query']
    url = reverse('search_user_topics',)
    query_params = {'q': query}
    return f"{url}?{urlencode(query_params)}"


class SearchUserTopicsView(LoginRequiredMixin, ListView):

  http_method_names = ['get']
  context_object_name = "topics"
  template_name = "search/search_your_topics.html"

  def get_full_text_search_queryset(self, cleaned_query):
    search_vector_fields = SearchVector("content", "title", config='english')
    search_query = SearchQuery(cleaned_query, search_type="websearch")
    search_content_headline = SearchHeadline(
      "content",
      search_query,
      start_sel='<span style="background-color: #FFFBC8;">',
      stop_sel='</span>',
      highlight_all=True,
    )
    search_title_headline = SearchHeadline(
      "title",
      search_query,
      start_sel='<span style="background-color: #FFFBC8;">',
      stop_sel='</span>',
      highlight_all=True,
    )
    topics = Topic.objects.annotate(
      search=search_vector_fields,
      rank=SearchRank(search_vector_fields, search_query, cover_density=True),
      search_content_highlight=search_content_headline,
      search_title_highlight=search_title_headline,
    ).filter(
      search_vector=search_query
    ).prefetch_related(
      'user', 'community',
    ).filter(
      user=self.request.user
    ).order_by(
      "-rank", "-created"
    )
    return topics
  
  def get_trigram_search_queryset(self, query, query_length):
    if query_length < 5:
      trigram_threshold = 0.2
    elif query_length <= 10:
      trigram_threshold = 0.3
    else:
      trigram_threshold = 0.4
    topics = Topic.objects.annotate(
      similarity=TrigramSimilarity('content', query) + TrigramSimilarity('title', query)
    ).filter(
      Q(similarity__gt=trigram_threshold)
    ).filter(
      user=self.request.user
    ).order_by(
      "-similarity"
    )
    for topic in topics:
      topic.search_content_highlight = highlight_text(topic.content, query)
      topic.search_title_highlight = highlight_text(topic.title, query)
    return topics

  def get_queryset(self):
    query = self.request.GET.get("q", "").strip()
    cleaned_query = remove_stop_words(query)
    topics = Topic.objects.none()
    if query:
      topics = self.get_full_text_search_queryset(cleaned_query)
      if not topics.exists():
        query_length = len(query.replace(" ", ""))
        topics = self.get_trigram_search_queryset(query, query_length)
    return topics
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    query = self.request.GET.get("q", "").strip()
    context["search_query"] = query
    context['search_count'] = self.get_queryset().count()
    return context


class NewSavedSearchFromKeywordView(LoginRequiredMixin, CreateView):

  model = SavedSearch
  form_class = NewSavedSearchFromKeywordModelForm
  http_method_names = ["get", "post",]
  # permission_required = ('accounts.full_access_to_entire_platform',)
  template_name = 'search/new_search_keyword.html'

  def form_valid(self, form):
    instance = form.save(commit=False)
    name = form.cleaned_data['name']
    form.instance.user = self.request.user
    form.instance.name = name
    form.save()

    if self.request.headers.get('HX-Request'):
      return HttpResponse(render_to_string('search/partials/saved_search_form.html', {'form': self.form_class()}))
    else:
      return HttpResponseRedirect(self.get_success_url())

  def get_success_url(self, **kwargs):
    return reverse_lazy('user_topics', kwargs={'username': self.request.user})


class SavedSearchesView(LoginRequiredMixin, ListView):

  http_method_names = ['get']
  context_object_name = "searches"
  template_name = "search/saved_searches.html"

  def get_queryset(self):
    searches = SavedSearch.objects.prefetch_related('user').filter(user=self.request.user)
    return searches


class DeleteSavedSearchView(LoginRequiredMixin, DeleteView):

  context_object_name = 'saved_search'
  http_method_names = ["post", "delete",]
  # permission_required = ('accounts.full_access_to_entire_platform',)

  def get_object(self, queryset=None):
    slug = self.kwargs.get('slug')
    saved_search = SavedSearch.objects.get(slug=slug, user=self.request.user)
    return saved_search

  def delete(self, request, *args, **kwargs):
    self.object = self.get_object()
    self.object.delete()

    if request.headers.get('HX-Request'):
      searches = SavedSearch.objects.filter(user=request.user)
      html = render_to_string(
        'search/partials/_saved_searches.html', {'searches': searches,}
      )
      return HttpResponse(html)
    return HttpResponseRedirect(self.get_success_url())

  def get_success_url(self, **kwargs):
    return reverse_lazy('saved_searches', kwargs={'username': self.request.user})


class SearchCategoryTopicsView(LoginRequiredMixin, ListView):

  http_method_names = ['get']
  context_object_name = "topics"
  template_name = "search/search_category_topics.html"