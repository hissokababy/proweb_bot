from django.contrib import admin

from tg_bot.models import Group, User, UserAdmin, MediaGroupPost, MediaGroupFile

# Register your models here.

admin.site.register(User)
admin.site.register(Group)


class MediaGroupFileInline(admin.TabularInline):
    fk_name = 'media_group'
    model = MediaGroupFile
    extra = 1


@admin.register(UserAdmin)
class UserAdminAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_confirm']


@admin.register(MediaGroupPost)
class MediaGroupPostAdmin(admin.ModelAdmin):
    list_display = ['id',]
    inlines = [MediaGroupFileInline,]