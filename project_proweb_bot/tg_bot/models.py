from django.db import models

from tg_bot.bot import bot
from common.texts import texts
from common.kbds import main_btns_inline

# Create your models here.

class User(models.Model):
    tg_id = models.PositiveBigIntegerField(primary_key=True)
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
                             reply_markup=main_btns_inline(self.user.language_selected, 'confirm_admin'))
            return 'Не подтверждено пользователем'
        else:
            return 'Подтверждено пользователем'

    class Meta:
        verbose_name = 'Администратора'
        verbose_name_plural = 'Администраторы'