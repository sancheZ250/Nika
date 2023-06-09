
from django.urls import re_path, path

from .views import add_news, NewsListView, NewsDetailView, search_news_view, delete_news

urlpatterns = [
    path('createnews/', add_news, name='new_news'),
    path('', NewsListView.as_view(), name='news'),
    path('news_details/<int:pk>', NewsDetailView.as_view(), name='news_details'),
    path('search/', search_news_view, name='search_news'),
    path('delete/<int:pk>/', delete_news, name='delete_news')
]