from django.conf.urls import url, include
from rest_framework_nested import routers
from django.urls import path

from . import views

router = routers.SimpleRouter()
router.register(r'games', views.GameViewSet)

games_router = routers.NestedSimpleRouter(router, r'games', lookup='game')
games_router.register(r'moves', views.MoveViewSet, base_name='game-moves')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(games_router.urls)),
]
