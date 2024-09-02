from django.contrib import admin
from users.models import User, Payments, Subscriptions
from lms.models import Course, Lesson


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'email', 'is_active', 'is_staff', 'is_superuser']


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ['pk', 'payment_sum', 'payment_method']


@admin.register(Course)
class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'description', 'owner', 'created_at', 'updated_at']


@admin.register(Lesson)
class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'lesson_name', 'lesson_description', 'course', 'owner']


@admin.register(Subscriptions)
class UserAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'last_date']
