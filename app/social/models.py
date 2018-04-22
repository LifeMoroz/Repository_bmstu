from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q

from app.library.constants import Access


class User(AbstractUser):
    gender = models.BooleanField('Пол', choices=((0, 'Женский'), (1, 'Мужской')))

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.get_full_name()

    def has_access(self, category):
        if category.access == Access.PUBLIC:
            return True
        if self.groups.filter(Q(name='Администраторы') | Q(name='Редакторы') ):
            return True
        return self.categories.filter(id=category.id, granted=True).exists()
