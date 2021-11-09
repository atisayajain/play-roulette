from rest_framework import routers
from django.urls import path, include

from . import views


urlpatterns = [
    path('dealer/<int:pk>/start', views.GameStartAPIView.as_view()),
    path('dealer/<int:pk>/end', views.GameEndAPIView.as_view()),
    path('dealer/<int:pk>/throw', views.BallThrowAPIView.as_view()),
    path('game/<int:pk>/bet', views.BetAPIView.as_view()),
]