from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from . import models

# Register your models here.


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    """Django cannot find our custom user by default
    """

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('birth_date', 'first_name', 'last_name',
                                        'email', 'phone_number',
                                        'street_address', 'city', 'country_code')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(models.Club)
@admin.register(models.Harbour)
@admin.register(models.Jetty)
class SimpleAdmin(admin.ModelAdmin):
    """Completely uncustomised admin
    """

    pass


@admin.register(models.Berth)
class BerthAdmin(admin.ModelAdmin):
    """Deal with field order
    """

    fieldsets = (
        (None, {'fields':
            ('name', 'jetty', 'boat'),
        }),
    )

