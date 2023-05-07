from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('categories', views.articles, name='categories'),
    path('article/<str:id>', views.blog, name='blog'),
    path('search', views.search, name='search'),
    path('getblog', views.getblog, name='getblog'),
]