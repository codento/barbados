from rest_framework.permissions import DjangoModelPermissions
from barbados.barbadosdb.models import User, Boat
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

    def _changes_permitted_fields(user, request):
        return True

    def has_permission(self, request, view):
        # Let the _own_ cases fall through to the has_object_permission checks
        if request.method == 'GET' and \
                re.match('/api/user/[0-9a-f\-]+/', request.path) \
                and request.user and request.user.has_perm('barbadosdb.view_own_user'):
            return True
        elif (request.method == 'PUT' or request.method == 'PATCH') and \
                re.match('/api/user/[0-9a-f\-]+/', request.path) and \
                request.user.has_perm('barbadosdb.change_own_user'):
            return True
        elif request.method == 'GET' and \
                re.match('/api/boat/[0-9a-f\-]+/', request.path) and \
                request.user.has_perm('barbadosdb.view_own_boat'):
            return True
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET' and \
                type(obj) == User and \
                not request.user.has_perm('barbadosdb.view_user') and \
                request.user.has_perm('barbadosdb.view_own_user') and \
                obj != request.user:
            return False
        elif (request.method == 'PUT' or request.method == 'PATCH') and \
                type(obj) == User and \
                not request.user.has_perm('barbadosdb.view_user') and \
                request.user.has_perm('barbadosdb.view_own_user') and \
                (obj != request.user or not self._changes_permitted_fields(obj, request)):
            return False
        elif request.method == 'GET' and \
                type(obj) == Boat and \
                not request.user.has_perm('barbadosdb.view_boat') and \
                request.user.has_perm('barbadosdb.view_own_boat') and \
                obj.user != request.user:
            return False
        return super().has_object_permission(request, view, obj)

