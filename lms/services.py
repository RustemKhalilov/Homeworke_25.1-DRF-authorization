from datetime import datetime, timedelta

import pytz
from django.shortcuts import get_object_or_404

from config import settings
from lms.models import Course
from users.models import Subscriptions


def get_email_list(pk):
    """Отправляет сообщение пользователю об обновлении курса"""
    subscriptions = Subscriptions.objects.filter(course=pk)

    course = get_object_or_404(Course, pk=pk)
    email_list = []
    message = f"Ваш курс {course.name} был обновлен!"
    for s in subscriptions:
        email_list.append(s.user.email)

        print(f"email added = {s.user.email}")

    return message, email_list
