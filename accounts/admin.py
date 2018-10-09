from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import (UserAdminCreationForm, UserAdminChangeForm)
from .models import CustomUser, UserProfile, InstituteProfile, UserFollow
from .models import CustomUser, UserProfile, InstituteProfile



class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    list_display = ('user_role', 'email', 'last_login', 'date_joined')
    list_filter = ('date_joined', 'last_login')

    fieldsets = (
        ('Login Credentials', {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('user_role', 'is_staff', 'is_superuser', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}),
    )

    search_fields = ('email',)
    ordering = ('last_login',)
    filter_horizontal = ()


admin.site.register(CustomUser, UserAdmin)

admin.site.unregister(Group)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'geder', 'date_of_birth', 'first_name', 'last_name')
    list_filter = ('user',)
    search_fields = ('email', 'first_name', 'last_name')


admin.site.register(UserProfile, ProfileAdmin)


class InstituteProfileAdmin(admin.ModelAdmin):
    list_display = ('institute', 'location', 'category', 'name')
    list_filter = ('institute', 'category', 'name')


admin.site.register(InstituteProfile, InstituteProfileAdmin)


class UserFollowAdmin(admin.ModelAdmin):
    list_display = ('following', 'followed', 'created_at')


admin.site.register(UserFollow, UserFollowAdmin)
