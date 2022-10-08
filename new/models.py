from django.db import models


# Create your models here.
class New(models.Model):
    name = models.CharField('Заголовок', max_length=100)
    text = models.TextField('Текст Новости')
    chance = models.DecimalField('Нейронка', max_digits=4, decimal_places=3)
    date_published = models.DateTimeField('Дата опубликования', auto_now_add=True)
    category_news = models.ForeignKey('Category_News', on_delete=models.PROTECT, verbose_name='Категория')
    img_news = models.ImageField(upload_to='photos/', verbose_name='Фото', blank=True)
    like = models.ForeignKey('likee', on_delete=models.CASCADE, verbose_name='Лайк', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Category_News(models.Model):
    category = models.CharField('Категория', max_length=100, db_index=True)

    def __str__(self):
        return self.category

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Crypta(models.Model):
    name = models.CharField('Заголовок', max_length=100)
    text = models.TextField('Текст Новости')
    date_published = models.DateTimeField('Дата опубликования', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'КриптоНовость'
        verbose_name_plural = 'КриптоНовости'


class Likee(models.Model):
    like = models.BooleanField('Лайк', blank=True)

    def __str__(self):
        return 'like'

    class Meta:
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'
