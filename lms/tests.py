from rest_framework.reverse import reverse
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Lesson, Course
from users.models import User

#
"""
Напишите тесты, которые будут проверять корректность работы CRUD уроков и функционал работы подписки на обновления курса.

В тестах используйте метод 
setUp
 для заполнения базы данных тестовыми данными. Обработайте возможные варианты взаимодействия с контроллерами пользователей с разными правами доступа. Для аутентификации пользователей используйте 
self.client.force_authenticate()
. Документацию к этому методу можно найти тут.
"""


class CoursesTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="user15@list.ru")

        self.course = Course.objects.create(name='Сопротивление материалов', description='Курс о свойствах '
                                                                                         'материалов и их работе при '
                                                                                         'нагружении', owner=self.user)

        video = "https://www.youtube.com/watch?v=_UZhalfqCfA&list=PLtaqFZsfPcLlQ4Jvdu9EWQF8iHi831mQa"

        self.lesson = Lesson.objects.create(lesson_name='Работа материалов при растяжении и сжатии', course=self.course,
                                            lesson_description="Урок изучает работу материалов при растяжении и сжатии волокн",
                                            lesson_url=video, owner=self.user)

        self.client.force_authenticate(user=self.user)

    def test_course_retrieve(self):
        url = reverse("lms:course-detail", args=(self.course.pk,))  # url lms:course-detail" в таком виде потому что
        # созданы на основе CourseViewSet
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name'), self.course.name)

    def test_course_create(self):
        url = reverse("lms:course-list")
        data = {"name": "Расчет статически неопределимых систем",
                "description": "Курс изучает расчеты статически неопределимых систем"
                }
        response = self.client.post(url, data)

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)  # Один курс создается выше в разделе setUp другой тут,
        # поэтому объектов во временной базе 2

    def test_course_update(self):
        url = reverse("lms:course-detail", args=(self.course.pk,))
        data = {"name": "Расчет статически определимых систем",
                "description": "Курс изучает расчеты статически неопределимых систем"
                }
        response = self.client.patch(url, data)

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name'), "Расчет статически определимых систем")

    def test_course_delete(self):
        url = reverse("lms:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)

    def test_course_list(self):
        url = reverse("lms:course-list")
        response = self.client.get(url)
        data = response.json()
        #print(data)
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.course.pk,
                    "name": self.course.name,
                    "preview": None,
                    "description": self.course.description,
                    "owner": self.user.pk
                }
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class LessonsTestCase(APITestCase):

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

    def test_lesson_retrieve(self):
        url = reverse("lms:lesson_retrive", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('lesson_name'), self.lesson.lesson_name)

    def test_lesson_create(self):
        url = reverse("lms:lesson_create")
        course_id = self.course.pk
        print(self.course.pk)

        data = {
            "lesson_name": "Группы Ассура различных видов",
            "lesson_description": "Урок рассматривает группы Ассура и их применение",
            "course": self.course.pk,
        }
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        url = reverse("lms:lesson_update", args=(self.lesson.pk,))
        data = {"lesson_name": "Группы Ассура базовых видов"}
        response = self.client.patch(url, data)

        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('lesson_name'), "Группы Ассура базовых видов")

    def test_lesson_delete(self):
        url = reverse("lms:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("lms:lesson_list")
        response = self.client.get(url)

        data = response.json()
        print(f"data {data}")

        result = {'count': 1,
                  'next': None,
                  'previous': None,
                  'results':
                      [
                          {'id': self.lesson.pk,
                           'lesson_name': self.lesson.lesson_name,
                           'lesson_description': self.lesson.lesson_description,
                           'lesson_preview': None,
                           'lesson_url': self.lesson.lesson_url,
                           'course': self.lesson.course.pk,
                           'owner': self.user.pk,
                           }
                      ]
                  }

        print(f"result {result}")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
