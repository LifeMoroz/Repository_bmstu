from django.contrib.auth.models import AbstractUser
from django.db import models

from app.library.constants import Access


class Category(models.Model):
    title = models.CharField(verbose_name='Название', max_length=255)
    ACCESS_CHOICES = ((Access.PRIVATE, 'Приватный'), (Access.PUBLIC, 'Публичный'))
    access = models.IntegerField(verbose_name='Уровень доступа', choices=ACCESS_CHOICES)
    users = models.ManyToManyField('social.User', through='UserCategory', related_name='accessed_categories')
    author = models.ForeignKey('social.User', models.CASCADE, verbose_name='Автор', related_name='categories')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'


class UserCategory(models.Model):
    user = models.ForeignKey(verbose_name='Автор запроса', to='social.User', on_delete=models.CASCADE)
    category = models.ForeignKey(verbose_name='Категория', to='Category', on_delete=models.CASCADE)
    granted = models.BooleanField('Доступ получен', default=False)

    class Meta:
        verbose_name = 'Права на раздел'
        verbose_name_plural = 'Права на разделы'

    def __str__(self):
        if not self.granted:
            title = 'Запрос на `{object}` от `{user}`'
        else:
            title = '`{object}` доступен для `{user}`'
        return title.format(object=self.category, user=self.user)
