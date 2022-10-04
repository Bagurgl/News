from django.shortcuts import render, HttpResponse

from .models import New


def index(request):
    news = New.objects.all()  # Сортировка: object.order_by(-name)         Филтр: object.filter(id=2)
    context = {
        'news__': news,
        'title': 'Новости ВТБ',
    }
    return render(request, 'new/index.html', context)


def index1(request):
    news = New.objects.all()  # Сортировка: object.order_by(-name)         Филтр: object.filter(id=2)
    context = {
        'news__': news,
        'title': 'Новости ВТБ',
    }
    return render(request, 'new/index1.html', context)


