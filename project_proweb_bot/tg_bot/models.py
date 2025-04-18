from django.db import models

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
    is_forwarding = models.CharField(max_length=255, verbose_name='Перессылка', blank=True, null=True)

    def __str__(self):
        return f'Пост {self.pk}, Тип {self.type}'

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class PostInChat(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='chats', blank=True, null=True)
    chat_tg_id = models.BigIntegerField(verbose_name='Тг ид группы в котором пост')
    message_id = models.BigIntegerField(verbose_name='Тг ид поста', unique=True)
    media_group_id = models.BigIntegerField(verbose_name='Ид медиа группы', blank=True, null=True)
    # main = models.BooleanField(default=Fa)

    def __str__(self):
        return f'Чат в котором пост {self.chat_tg_id}'
    
    class Meta:
        verbose_name = 'Чат в котором пост'
        verbose_name_plural = 'Чаты в котором посты'


class MediaGroupFile(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='files')
    type = models.CharField(verbose_name='Тип медиа', max_length=150, blank=True, null=True)
    media_id = models.TextField(verbose_name='Ид медиа файла')
    message_id = models.BigIntegerField(verbose_name='Тг ид сообщения', blank=True, null=True)

    def __str__(self):
        return f'Файл медиа-группы {self.type}'
    
    class Meta:
        verbose_name = 'Файл медиа-группы'
        verbose_name_plural = 'Файлы медиа-групп'
