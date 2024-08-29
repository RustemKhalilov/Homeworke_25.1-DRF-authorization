from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny

from users.models import Payments, User, Subscriptions
from users.serializers import PaymentsSerializer, UserSerializer, SubscriptionsSerializer
from users.services import create_stripe_price, create_stripe_session


class PaymentsListAPIView(generics.ListAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ('paid_lesson', 'paid_course', 'payment_method')
    ordering_fields = ('date_payment')


class PaymentsCreateAPIView(CreateAPIView):
    serializer_class = PaymentsSerializer
    queryset = Payments.objects.all()
    
    def perform_create(self, serializer):
        payment = serializer.save()#user=self.request.user
        price = create_stripe_price(payment.payment_sum)
        session_id, payment_link = create_stripe_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class SubscriptionsCreateAPIView(CreateAPIView):
    queryset = Subscriptions.objects.all()
    serializer_class = SubscriptionsSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SubscriptionsDestroyAPIView(DestroyAPIView):
    queryset = Subscriptions.objects.all()