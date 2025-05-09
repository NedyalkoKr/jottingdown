""" URL configuration for jottingdown project. """

from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from accounts.views import UserLoginView, UserLogoutView


if settings.DEBUG:
    import debug_toolbar
    debug_urls = [path('debug/', include(debug_toolbar.urls)),]
    admin_urls = [path('admin/', admin.site.urls)]
    # reload_urls = [path("__reload__/", include("django_browser_reload.urls"))]
    # flatpages_urls = [path(route='pages/', view=include('django.contrib.flatpages.urls')),]
else:
    admin_urls = [path('admince8d3121c361928100adfd1438ac87a8c89e35c4/', admin.site.urls)]


urlpatterns = [
    path(route='login/', view=UserLoginView.as_view(), name='user_login'),
    path(route='logout/', view=UserLogoutView.as_view(), name='user_logout'),
    path(route='account/', view=include('accounts.urls.account_urls')),
    path(route='profile/', view=include('accounts.urls.profile_urls')),
    path(route='settings/', view=include('accounts.urls.settings_urls')),
    path(route='topic/', view=include('topics.urls.topic_urls')),
    path(route='topics/', view=include('topics.urls.topics_urls')),
    path(route='posts/', view=include('topics.urls.posts_urls')),
    path(route='communities/', view=include('core.urls.communities_urls')),
    path(route='community/', view=include('core.urls.community_urls')),
    path(route='category/', view=include('core.urls.category_urls')),
    path(route='follow/', view=include('follow.urls.follow_urls')),
    path(route='unfollow/', view=include('follow.urls.unfollow_urls')),
    path(route='search/', view=include('search.urls.search_urls')),
    path(route='comment/', view=include('comments.urls.comment_urls')),
    path(route='comments/', view=include('comments.urls.comments_urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns = urlpatterns + admin_urls + debug_urls + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns = urlpatterns + admin_urls