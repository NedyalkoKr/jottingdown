from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.db.models import Func, F, Q, Value, CharField, FloatField, Count, TextField, Max
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank, SearchHeadline, TrigramSimilarity, TrigramWordSimilarity
from core.models import Community
from topics.models import Topic
from search.models import SearchHistory

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
    similarity_threshold = 0.5 if query_length < 5 else 0.6 if query_length <= 10 else 0.7

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
  template_name = "search/search_topics.html"

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
  context_object_name = "posts"
  template_name = "search/search_all_topics.html"

  def update_search_history(self, cleaned_query):
    """Update or create search history entry for the given query."""
    obj, created = SearchHistory.objects.get_or_create(query=cleaned_query)
    if not created:
      obj.search_count = F('search_count') + 1
      obj.save(update_fields=['search_count'])
    else:
      obj.search_count = 1
      obj.save(update_fields=['search_count'])

  def get_full_text_search_queryset(self, cleaned_query):
    search_vector_fields = SearchVector("content", "title", config='english')
    search_query = SearchQuery(cleaned_query, search_type="websearch")
    search_headline = SearchHeadline(
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
      content_highlight=search_headline,
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
    if query_length < 5:
      trigram_threshold = 0.2
    elif query_length <= 10:
      trigram_threshold = 0.3
    else:
      trigram_threshold = 0.4
    
    topic = Topic.objects.annotate(
      similarity=TrigramSimilarity('content', query) + TrigramSimilarity('title', query)
    ).filter(
      Q(similarity__gt=trigram_threshold)
    ).exclude(
      user=self.request.user
    ).order_by(
      "-similarity"
    )
    for topic in topic:
      topic.content_highlight = highlight_text(topic.content, query)
      topic.search_title_highlight = highlight_text(topic.title, query)
    return topic

  def get_queryset(self):
    query = self.request.GET.get("sq", "").strip()
    cleaned_query = remove_stop_words(query)
    topics = Topic.objects.none()
    if query:
      self.update_search_history(cleaned_query)
      topics = self.get_full_text_search_queryset(cleaned_query)
      if not topics.exists():
        query_length = len(query.replace(" ", ""))
        topics = self.get_trigram_search_queryset(query, query_length)
    return topics
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    query = self.request.GET.get("sq", "").strip()
    context["search_query"] = query
    return context