from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()

router.register(r'player', views.PlayerAPIView)


urlpatterns = [
    path('player/<int:pk>/casino', views.PlayerCasinoAPIView.as_view()),
    path('player/<int:pk>/games', views.BettableGamesAPIView.as_view()),
    path('', include(router.urls)),
]