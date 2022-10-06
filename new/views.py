from django.shortcuts import render, HttpResponse

from .models import *


def index(request):
    news = New.objects.all()  # Сортировка: object.order_by(-name)         Филтр: object.filter(id=2)
    context = {
        'news__': news,
        'title': 'Новости ВТБ',
    }
    return render(request, 'new/index.html', context)


def index1(request):
    news = New.objects.all()  # Сортировка: object.order_by(-name)         Филтр: object.filter(id=2)
    cat = Category_News.objects.all()
    context = {
        'news__': news,
        'title': 'Новости ВТБ',
        'category': cat,
    }
    return render(request, 'new/index1.html', context)


def get_category(request, category_news_id):
    news = New.objects.filter(category_news_id=category_news_id)
    cats = Category_News.objects.all()
    category = Category_News.objects.get(pk=category_news_id)
    return render(request, 'new/category.html', {'news': news, 'cats': cats,
                                                 'category': category})