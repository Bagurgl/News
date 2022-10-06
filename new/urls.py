from django.urls import path

from .views import *

urlpatterns = [
    path('', index),
    path('home/', index1),
    path('category/<int:category_news_id>/', get_category),
]

