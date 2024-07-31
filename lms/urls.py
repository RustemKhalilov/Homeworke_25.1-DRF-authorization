from rest_framework.routers import SimpleRouter

from lms.views import CourseViewSet, LessonCreateApiView, LessonListApiView, LessonUpdateApiView, LessonRetriveApiView, LessonDestroyApiView

from lms.apps import LmsConfig

from django.urls import path

app_name = LmsConfig.name


router = SimpleRouter()
router.register("", CourseViewSet)

urlpatterns = [
    path("lessons/", LessonListApiView.as_view(), name="lesson_list"),
    path("lessons/<int:pk>/", LessonRetriveApiView.as_view(), name="lesson_retrive"),
    path("lessons/create/", LessonCreateApiView.as_view(), name="lesson_create"),
    path("lessons/<int:pk>/delete/", LessonDestroyApiView.as_view(), name="lesson_delete"),
    path("lessons/<int:pk>/update/", LessonUpdateApiView.as_view(), name="lesson_update"),
]

urlpatterns += router.urls