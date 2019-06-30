# Register your models here.

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('nim', 'name')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nim', 'name', 'password1', 'password2'),
        }),
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('nim', 'first_name', 'last_name', 'name')
    ordering = ('nim',)
    filter_horizontal = ('groups', 'user_permissions',)

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('name', 'nim')

admin.site.register(CustomUser, CustomUserAdmin)