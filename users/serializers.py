from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from users.models import User, Payments, Subscriptions


class UserSerializer(ModelSerializer):
    payments = SerializerMethodField(read_only=True)
    subscriptions = SerializerMethodField(read_only=True)

    def get_payments(self, obj):
        return [
            f"{p.date_of_payment}-({p.payment_amount}, наличные: {p.payment_method_is_cash}),"
            for p in Payments.objects.filter(user=obj).order_by("date_of_payment")
        ]

    def get_subscriptions(self, obj):
        return [
            f"{s.course}-(pk={s.course.pk}{bool(s.last_date < s.course.updated_at) * ' Курс обновлен!'}),"
            for s in Subscriptions.objects.filter(user=obj).order_by("last_date")
        ]

    class Meta:
        model = User
        fields = "__all__"


class PaymentsSerializer(ModelSerializer):
    class Meta:
        model = Payments
        fields = "__all__"


class SubscriptionsSerializer(ModelSerializer):
    class Meta:
        model = Subscriptions
        fields = "__all__"
