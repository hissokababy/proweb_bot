from django.contrib import admin

from tg_bot.models import Group, User, UserAdmin

# Register your models here.

admin.site.register(User)
admin.site.register(Group)


@admin.register(UserAdmin)
class UserAdminAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_confirm']
