from rest_framework import routers
from . import api_views

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'user', api_views.UserViewSet)
router.register(r'boat', api_views.BoatViewSet)
router.register(r'club', api_views.ClubViewSet)
router.register(r'harbour', api_views.HarbourViewSet)
router.register(r'jetty', api_views.JettyViewSet)
router.register(r'berth', api_views.BerthViewSet)
