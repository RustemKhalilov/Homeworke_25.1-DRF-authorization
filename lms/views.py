import pytz
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from config import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView

from lms.models import Lesson, Course
from lms.paginations import CustomPagination
from lms.serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer
from users.permissions import IsModer, IsOwner
from lms.tasks import send_information_about_course_update


class CourseViewSet(ModelViewSet):
    """
    Для POST запроса если он правильно сфоримрован например в POSTMAN создат объект
    Для GET запроса в нашем случае  http://127.0.0.1:8000/lms/ вернет количество объектов Course в базе данных
    Поэтому отдельный класс для создания объекта Course можно не делать
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    # Чтобы выводить нужный серриалайзер нужно переопределить метод
    def get_serializer_class(self):
        if self.action == "retrieve":
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        # print(f'!!!!!!{self.action_map}')
        for item, value in self.action_map.items():
            if value == self.action:
                if value == "create":
                    self.permission_classes = (~IsModer,)
                elif value in ["update", "retrieve", "partial_update"]:
                    self.permission_classes = (IsModer | IsOwner,)
                elif value == "destroy":
                    self.permission_classes = (IsOwner | ~IsModer,)
                elif value != "create":
                    self.permission_classes = (IsOwner,)
                return super().get_permissions()


class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModer, IsAuthenticated)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        zone = pytz.timezone(settings.TIME_ZONE)
        current_datetime_4_hours_ago = datetime.now(zone) - timedelta(minutes=1)# timedelta(hours=4)

        course = get_object_or_404(Course, pk=lesson.course.pk)

        if lesson.course.updated_at < current_datetime_4_hours_ago:
            send_information_about_course_update.delay(course.pk)

        lesson.save(())


class LessonListApiView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination


class LessonRetriveApiView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonUpdateApiView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsOwner | ~IsModer)
