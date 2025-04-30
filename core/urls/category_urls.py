from django.urls import path
from ..views import CategoryView

urlpatterns = [
  path(route='<slug:slug>/', view=CategoryView.as_view(), name='category')
]