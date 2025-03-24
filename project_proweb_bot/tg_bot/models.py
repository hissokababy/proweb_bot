from django.db import models

from tg_bot.bot import bot
from common.texts import texts
from common.kbds import main_btns_reply

# Create your models here.

class User(models.Model):
    tg_id = models.PositiveBigIntegerField(verbose_name='Тг ид пользователя', unique=True)
    username = models.CharField(max_length=150, verbose_name='Юзер пользователя', blank=True, null=True)
    language_selected = models.CharField(choices={'ru': 'Russian', 'uz': 'Uzbek'}, max_length=15, default='ru', 
                                         verbose_name='Выбранный язык')

    def __str__(self):
        return f'{self.tg_id} {self.username}'
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class UserAdmin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    confirmed_by_user = models.BooleanField(default=False, verbose_name='Подтверждён пользователем')

    def __str__(self):
        return f'Администратор {self.user.tg_id} {self.user.username}'
    
    def get_confirm(self):
        if self.confirmed_by_user == False:
            bot.send_message(self.user.tg_id, texts[self.user.language_selected]['confirm_admin'], 
                             reply_markup=main_btns_reply(self.user.language_selected, 'confirm_admin'))
            return 'Не подтверждено пользователем'
        else:
            return 'Подтверждено пользователем'

    class Meta:
        verbose_name = 'Администратора'
        verbose_name_plural = 'Администраторы'


class Group(models.Model):
    tg_id = models.BigIntegerField(verbose_name='Тг ид группы', unique=True)
    course = models.CharField(max_length=150, verbose_name='Курс группы')
    language = models.CharField(max_length=150, verbose_name='Язык группы')
    days = models.CharField(max_length=150, verbose_name='Дни обучения группы')
    time = models.CharField(max_length=150, verbose_name='Время обучения группы')

    def __str__(self):
        return f'{self.pk} {self.course} {self.language} {self.days} {self.time}'
    
    class Meta:
        verbose_name = 'Группу'
        verbose_name_plural = 'Группы'