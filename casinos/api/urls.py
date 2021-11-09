from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()

router.register(r'casino', views.CasinoAPIView)


urlpatterns = [
    path('casino/<int:pk>/dealer', views.CasinoDealerAPIView.as_view()),
    path('', include(router.urls)),
]