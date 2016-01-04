from rest_framework.permissions import DjangoModelPermissions
from barbados.barbadosdb.models import User, Boat, Berth
import re


class ModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    _USER_OWN_PERMITTED_FIELDS = ['phone_number', 'street_address', 'city', 'country_code']

    def _changes_only_fields(self, request, obj, permitted_field_names):
        for field_name in request.data.keys():
            if field_name not in permitted_field_names:
                new_field_value = request.data[field_name]
                existing_field_value = getattr(obj, field_name, None)
                # This next test is risky, but luckily in our applcation non-URL values won't
                # generally look like URLs
                if new_field_value and re.match('^http', new_field_value):
                    # It's a URL field, extract the id
                    new_field_value_id = re.findall(r'/(.[0-9a-f\-]+)/$', new_field_value)[0]
                    if new_field_value_id != str(existing_field_value.id):
                        return False
                else:
                    if new_field_value != existing_field_value:
                        return False
        return True

    def _changes_only_field(self, request, obj, permitted_field_name):
        return self._changes_only_fields(request, obj, [permitted_field_name])

    def has_permission(self, request, view):
        # Let the _own_ cases fall through to the has_object_permission checks
        if request.method == 'GET' and \
                re.match('/api/user/[0-9a-f\-]+/', request.path) \
                and request.user and \
                not request.user.has_perm('barbadosdb.view_user') and \
                request.user.has_perm('barbadosdb.view_own_user'):
            return True
        elif (request.method == 'PUT' or request.method == 'PATCH') and \
                re.match('/api/user/[0-9a-f\-]+/', request.path) and \
                request.user and \
                not request.user.has_perm('barbadosdb.change_user') and \
                request.user.has_perm('barbadosdb.change_own_user'):
            return True
        elif request.method == 'GET' and \
                re.match('/api/boat/[0-9a-f\-]+/', request.path) and \
                request.user and \
                not request.user.has_perm('barbadosdb.view_boat') and \
                request.user.has_perm('barbadosdb.view_own_boat'):
            return True
        elif (request.method == 'PUT' or request.method == 'PATCH') and \
                re.match('/api/boat/[0-9a-f\-]+/', request.path) and \
                request.user and \
                not request.user.has_perm('barbadosdb.change_boat') and \
                request.user.has_perm('barbadosdb.assign_berth_boat'):
            return True
        elif (request.method == 'PUT' or request.method == 'PATCH') and \
                re.match('/api/berth/[0-9a-f\-]+/', request.path) and \
                request.user and \
                not request.user.has_perm('barbadosdb.change_berth') and \
                request.user.has_perm('barbadosdb.assign_berth_boat'):
            return True
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET' and \
                type(obj) == User and \
                request.user and \
                not request.user.has_perm('barbadosdb.view_user') and \
                request.user.has_perm('barbadosdb.view_own_user') and \
                obj != request.user:
            return False
        elif (request.method == 'PUT' or request.method == 'PATCH') and \
                type(obj) == User and \
                request.user and \
                not request.user.has_perm('barbadosdb.change_user') and \
                request.user.has_perm('barbadosdb.change_own_user') and \
                (obj != request.user or
                 not self._changes_only_fields(request, obj, self._USER_OWN_PERMITTED_FIELDS)):
            return False
        elif request.method == 'GET' and \
                type(obj) == Boat and \
                request.user and \
                not request.user.has_perm('barbadosdb.view_boat') and \
                request.user.has_perm('barbadosdb.view_own_boat') and \
                obj.user != request.user:
            return False
        elif (request.method == 'PUT' or request.method == 'PATCH') and \
                type(obj) == Boat and \
                request.user and \
                not request.user.has_perm('barbadosdb.change_boat') and \
                request.user.has_perm('barbadosdb.assign_berth_boat') and \
                not self._changes_only_field(request, obj, 'berth'):
            return False
        elif (request.method == 'PUT' or request.method == 'PATCH') and \
                type(obj) == Berth and \
                request.user and \
                not request.user.has_perm('barbadosdb.change_berth') and \
                request.user.has_perm('barbadosdb.assign_berth_boat') and \
                not self._changes_only_field(request, obj, 'boat'):
            return False
        return super().has_object_permission(request, view, obj)

