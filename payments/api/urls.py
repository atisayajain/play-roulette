from django.urls import path, include

from . import views


urlpatterns = [
    path('<account_type>/<int:pk>/recharge', views.RechargeAPIView.as_view()),
    path('<account_type>/<int:pk>/cashout', views.CashoutAPIView.as_view()),
    path('<account_type>/<int:pk>/balance', views.BalanceAPIView.as_view()),
]