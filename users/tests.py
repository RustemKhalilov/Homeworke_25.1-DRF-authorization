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
        self.user = User.objects.create(email="admin@sky.pro")

        self.course = Course.objects.create(title='Курс номер 1', description='Описание курса номер 1', owner=self.user)

        video = "https://www.youtube.com/watch?v=uC0jJGfDxtM&list=PLlb7e2G7aSpTFea2FYxp7mFfbZW-xavhL&index=1"

        self.lesson = Lesson.objects.create(title='Урок номер 1', course=self.course, description="описание",
                                            video_url=video, owner=self.user)

        self.client.force_authenticate(user=self.user)

        self.subscriptions = Subscriptions.objects.create(user=self.user, course=self.course)

    # def test_lesson_retrieve(self):
    #     url = reverse("courses:lessons-retrieve", args=(self.lesson.pk,))
    #     response = self.client.get(url)
    #     data = response.json()
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(data.get('title'), self.lesson.title)

    def test_subscription_create(self):
        url = reverse("users:subscriptions-create")
        # course_id = self.course.pk
        # print(self.course.pk)

        data = {
            "user": self.user.pk,
            "course": self.course.pk
        }

        response = self.client.post(url, data)

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 1)

    # def test_lesson_update(self):
    #     url = reverse("courses:lessons-update", args=(self.lesson.pk,))
    #     data = {"title": "Updated lesson"}
    #     response = self.client.patch(url, data)
    #
    #     data = response.json()
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(data.get('title'), "Updated lesson")

    def test_subcription_delete(self):
        url = reverse("users:subscriptions-delete", args=(self.subscriptions.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 1)

    # def test_lesson_list(self):
    #     url = reverse("courses:lessons-list")
    #     response = self.client.get(url)
    #
    #     data = response.json()
    #     # print(f"data {data}")
    #
    #
    #     result = {'count': 1,
    #          'next': None,
    #          'previous': None,
    #          'results':
    #              [
    #                  {'id': self.lesson.pk,
    #                   'title': self.lesson.title,
    #                   'description': self.lesson.description,
    #                   'preview': None,
    #                   'video_url': self.lesson.video_url,
    #                   'course': self.lesson.course.pk,
    #                   'owner':  self.user.pk,
    #                   }
    #              ]
    #          }
    #
    #     # print(f"result {result}")
    #
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(data, result)
    #
