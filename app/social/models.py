from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Q

from app.library.constants import Access
from app.social.constants import Position


class User(AbstractUser):
    gender = models.BooleanField('Пол', choices=((False, 'Женский'), (True, 'Мужской')))

    POSITION_CHOICES = ((Position.STUDENT, 'Студент'), (Position.TEACHER, 'Преподаватель'), (Position.PHD_STUDENT, 'Аспирант'))
    position = models.IntegerField('Должность', choices=POSITION_CHOICES)

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
