from django.contrib.auth.admin import UserAdmin
from django.core.urlresolvers import reverse
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
class ClubAdmin(admin.ModelAdmin):
    """Club administration
    """

    list_display = ('name',)


@admin.register(models.Harbour)
class HarbourAdmin(admin.ModelAdmin):
    """Harbours
    """

    list_display = ('name', 'club')


@admin.register(models.Jetty)
class JettyAdmin(admin.ModelAdmin):
    """Administer jetties
    """

    list_display = ('name', 'harbour')


@admin.register(models.Berth)
class BerthAdmin(admin.ModelAdmin):
    """Deal with field order
    """

    # XXX: This is probably a database hammer
    list_display = ('name', 'jetty', lambda self: self.jetty.harbour)

    fieldsets = (
        (None, {'fields':
            ('name', 'jetty', 'boat'),
        }),
    )


@admin.register(models.Boat)
class BoatAdmin(admin.ModelAdmin):
    """The thing that floats
    """

    def edit_link(self):
        """Name and registration can be empty but we need access
        """

        return '<a href={}>Edit</a>'.format(reverse('admin:barbadosdb_boat_change', args=(self.pk,)))
    edit_link.allow_tags = True
    edit_link.short_description = _('Edit link')

    list_display = ('name', 'registration_number', 'sail_number', 'user', edit_link)

