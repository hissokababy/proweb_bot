from django.db import models

from tg_bot.bot import bot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
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
            bot.send_message(self.user.tg_id, '<b>PROWEB</b> хочет назначить вас администратором, по подтверждаете?',
                             reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Да, подтверждаю ✅', callback_data='confirm')))
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
    is_in_group = models.BooleanField(default=False, verbose_name='Бот в группе')

    def __str__(self):
        return f'{self.pk} {self.course} {self.language} {self.days} {self.time}, В группе: {self.is_in_group}'
    
    class Meta:
        verbose_name = 'Группу'
        verbose_name_plural = 'Группы'



class Post(models.Model):
    caption = models.TextField(verbose_name='Текст поста', blank=True, null=True)
    type = models.CharField(max_length=150, verbose_name='Тип поста', null=True)
    post_tg_id = models.CharField(max_length=455, verbose_name='Тг ид поста')
    media_id = models.CharField(max_length=455, verbose_name='Тг ид медиа файла', null=True, blank=True)
    media_group_id = models.BigIntegerField(verbose_name='Ид медиа группы', blank=True, null=True)
    sent_to_owner = models.BooleanField(default=False, verbose_name='Отправлен отправителю')

    def __str__(self):
        return f'Пост {self.pk}, Тип {self.type}'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class MediaGroupFile(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='files')
    type = models.CharField(verbose_name='Тип медиа', max_length=150, blank=True, null=True)
    media_id = models.TextField(verbose_name='Ид медиа файла')

    def __str__(self):
        return f'Файл медиа-группы {self.type}'
    
    class Meta:
        verbose_name = 'Файл медиа-группы'
        verbose_name_plural = 'Файлы медиа-групп'