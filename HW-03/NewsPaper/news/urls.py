from django.urls import path
# Импортируем созданное нами представление
from .views import NewsList, NewsDetail
from .models import Post


urlpatterns = [
   path('', NewsList.as_view(), name='news'),
   path('<int:pk>', NewsDetail.as_view()),
]