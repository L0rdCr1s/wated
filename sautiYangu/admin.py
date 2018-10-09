from django.contrib import admin
from .models import Category, Notification, NotifyUser


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('name',)


admin.site.register(Category, CategoriesAdmin)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'text')
    list_filter = ('created_at',)


admin.site.register(Notification, NotificationAdmin)


class NotifyUserAdmin(admin.ModelAdmin):
    list_display = ('target_user', 'user_notification', 'read')
    list_filter = ('read',)


admin.site.register(NotifyUser, NotifyUserAdmin)
