from django.urls import path

from .views import *

urlpatterns = [
    path('', index1, name='home'),
    path('category/<int:category_news_id>/', get_category, name='category'),
    path('news/<int:new_id>', get_new, name='new'),
]
