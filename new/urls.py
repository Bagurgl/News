from django.urls import path

from .views import *

urlpatterns = [
    path('', index1),
    path('category/<int:category_news_id>/', get_category, name='category'),
]

