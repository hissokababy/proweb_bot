from django.contrib import admin
from tg_bot.models import Group, User, UserAdmin, Post, MediaGroupFile

from tg_bot.services.admin import make_admin
# Register your models here.

admin.site.register(User)
admin.site.register(Group)


class MediaGroupFileInline(admin.TabularInline):
    fk_name = 'post'
    model = MediaGroupFile
    extra = 1


@admin.register(UserAdmin)
class UserAdminAdmin(admin.ModelAdmin):
    list_display = ['user']

    actions = ["make_admin", 'remove_admin']

    @admin.action(description="Назначить админом")
    def make_admin(self, request, queryset):
        make_admin(queryset)


@admin.register(Post)
class MediaGroupPostAdmin(admin.ModelAdmin):
    list_display = ['id', 'type']
    inlines = [MediaGroupFileInline,]