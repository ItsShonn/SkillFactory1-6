from ast import Index

from django.urls import path
# Импортируем созданное нами представление
from .views import (NewsList, NewsDetail, SearchList, NewsCreate, ArticleCreate,
                    NewsDelete, NewsUpdate, ArticleDelete, ArticleUpdate, upgrade_me, IndexView, CategoryList,
                    subscribe)
from .models import Post


urlpatterns = [
   path('', IndexView.as_view(), name='home'),
   path('news/', NewsList.as_view(), name='news'),
   path('news/<int:pk>', NewsDetail.as_view(), name='news_detail'),
   path('news/search/', SearchList.as_view(), name='search'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('articles/create/', ArticleCreate.as_view(), name='articles_create'),
   path('articles/<int:pk>/update/', ArticleUpdate.as_view(), name='articles_update'),
   path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='articles_delete'),
   path('upgrade/', upgrade_me, name='upgrade'),
   path('category/', CategoryList.as_view() ,name='categories'),
   path('category/subscribe/<int:id>', subscribe, name='sub'),
]