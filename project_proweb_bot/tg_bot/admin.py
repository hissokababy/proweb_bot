from django.contrib import admin

from tg_bot.models import User, UserAdmin

# Register your models here.

admin.site.register(User)


@admin.register(UserAdmin)
class UserAdminAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_confirm']
