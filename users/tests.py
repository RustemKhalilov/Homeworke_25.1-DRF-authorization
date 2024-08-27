from rest_framework.reverse import reverse
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Lesson, Course
from users.models import User, Subscriptions

"""
path("subscriptions/create/", SubscriptionsCreateAPIView.as_view(), name="subscriptions_create"),
path("subscriptions/<int:pk>/delete/", SubscriptionsDestroyAPIView.as_view(), name="subscriptions_delete")
"""


class SubscriptionsTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@example.com")

        self.course = Course.objects.create(name='Сопротивление материалов', description='Курс о свойствах '
                                                                                         'материалов и их работе при '
                                                                                         'нагружении', owner=self.user)

        video = "https://www.youtube.com/watch?v=_UZhalfqCfA&list=PLtaqFZsfPcLlQ4Jvdu9EWQF8iHi831mQa"

        self.lesson = Lesson.objects.create(lesson_name='Работа материалов при растяжении и сжатии', course=self.course,
                                            lesson_description="Урок изучает работу материалов при растяжении и сжатии волокн",
                                            lesson_url=video, owner=self.user)

        self.client.force_authenticate(user=self.user)

        self.subscriptions = Subscriptions.objects.create(user=self.user, course=self.course)

    def test_subscription_create(self):
        url = reverse("users:subscriptions-create")

        data = {
            "user": self.user.pk,
            "course": self.course.pk
        }

        response = self.client.post(url, data)

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 1)

    def test_subcription_delete(self):
        url = reverse("users:subscriptions-delete", args=(self.subscriptions.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 1)
