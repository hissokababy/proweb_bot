from django.db import models

# Create your models here.


class User(models.Model):
    tg_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=150, verbose_name='Юзер пользователя', blank=True, null=True)
    first_name = models.CharField(max_length=150, verbose_name='Имя пользователя', blank=True, null=True)
    last_name = models.CharField(max_length=150, verbose_name='Фамилия пользователя', blank=True, null=True)
    phone_number = models.CharField(max_length=30, verbose_name='Номер телефон пользователя', blank=True, null=True)

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'