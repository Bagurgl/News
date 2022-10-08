from django.shortcuts import render, HttpResponse

from .models import *


def index1(request):
    news = New.objects.all()  # Сортировка: object.order_by(-name)         Филтр: object.filter(id=2)
    cat = Category_News.objects.all()
    context = {
        'news': news,
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


def get_new(request, new_id):
    new = New.objects.filter(pk=new_id)
    cats = Category_News.objects.all()
    if request.method == 'POST':
        New.like = True
    return render(request, 'new/get_new.html', {'new': new, 'cats': cats})

