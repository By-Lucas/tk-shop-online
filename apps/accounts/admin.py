from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from accounts.models import User
from accounts.forms import UserForm


class CustomUserAdmin(UserAdmin):
    list_display = ['name', 'email', 'is_superuser', 'is_staff']
    list_filter = []
    search_fields = ['name', 'email']
    filter_horizontal = []
    fieldsets = (
        (None, {'fields': ('name', 'email', 'username', 'password', 'is_company', 'is_active', 'is_staff', 'is_superuser', 'is_admin', 'user_system')}),
        
    )
    add_fieldsets = ((None, {'classes': ('wide',), 'fields': (
        'name', 'user_charisma', 'username', 'email', 'password1', 'password2',
    )}),)
    forms = UserForm

admin.site.register(User, CustomUserAdmin)
