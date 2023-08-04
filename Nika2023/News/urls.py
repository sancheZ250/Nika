
from django.urls import re_path, path, include
from .views import add_news, NewsListView, NewsDetailView, search_news_view, delete_news, NewsViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'news', NewsViewSet, basename='news')
urlpatterns = [
    path('createnews/', add_news, name='new_news'),
    path('', NewsListView.as_view(), name='news'),
    path('news_details/<int:pk>/', NewsDetailView.as_view(), name='news_details'),
    path('search/', search_news_view, name='search_news'),
    path('delete/<int:pk>/', delete_news, name='delete_news'),
    # path('api/v1/newslist/', NewsViewSet.as_view({'get': 'list'})),
    # path('api/v1/newslist/<int:pk>/', NewsViewSet.as_view({'put': 'update'})),
    path('api/v1/', include(router.urls)),
    path('api/v1/drf-auth/', include('rest_framework.urls')),
    path('api/v1/auth/', include('djoser.urls')), #djoser-auth by token
    re_path(r'^auth/', include('djoser.urls.authtoken')),
]