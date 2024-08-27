from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.apps import UsersConfig
from users.views import UserCreateAPIView, PaymentsListAPIView, PaymentsCreateAPIView, SubscriptionsCreateAPIView, \
    SubscriptionsDestroyAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=(AllowAny,)), name='token_refresh'),
    # payments
    path('payments/', PaymentsListAPIView.as_view(), name='payments'),
    path('payments/create/', PaymentsCreateAPIView.as_view(), name='payments_create'),
    # subscriptions
    path("subscriptions/create/", SubscriptionsCreateAPIView.as_view(), name="subscriptions-create"),
    path("subscriptions/<int:pk>/delete/", SubscriptionsDestroyAPIView.as_view(), name="subscriptions-delete")
]