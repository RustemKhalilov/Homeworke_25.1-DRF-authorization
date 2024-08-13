from rest_framework.serializers import ModelSerializer, SerializerMethodField

from lms.models import Lesson, Course


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"

class LessonSerializer(ModelSerializer):
    #course = CourseSerializer()
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    """
    Добавляем кастомное поле
    """
    course_count = SerializerMethodField()

    lesson_count = SerializerMethodField()

    lessons = SerializerMethodField()
    def get_course_count(t1, t2):
        return Course.objects.all().count()
    """
    Почему нужен второй парамет, потому что структура следующая
    в name вернется словарь Course:<Coures:.......>
    в self информация о сериализаторе  и много чего другого
    Короче если просто писать self без второго атрибута эта штука не работает
    можно написать t1, t2 тогда в первый аргумент все равно вернет self, во второй объект курса название и описание 

    в t1 - Value
    CourseDetailSerializer(<Course: Проектирование месторождений газа нефти: Курс рассматривает базовые принципы проектирования месторождений нефти и газа>, context={'request': <rest_framework.request.Request: GET '/lms/1/'>, 'format': None, 'view': <lms.views.CourseViewSet object>}):
    name = CharField(help_text='введите название курса', label='Название курса', max_length=100)
    description = CharField(allow_blank=True, allow_null=True, help_text='введите описание курса', label='Описание курса', required=False, style={'base_template': 'textarea.html'})
    owner = PrimaryKeyRelatedField(allow_null=True, label='Владелец курса', queryset=User.objects.all(), required=False)
    course_count = SerializerMethodField()
    в t2 - Value
    <Course: Проектирование месторождений газа нефти: Курс рассматривает базовые принципы проектирования месторождений нефти и газа>
    В общем возвращаются сложные объекты, которые можно рассмотреть на точке останова, ключающих много разных полей
    """
    def get_lesson_count(t1, t2):
        return Lesson.objects.all().filter(course=t2).count()

    """
    Почему нужен второй парамет, потому что структура следующая
    в name вернется словарь Course:<Coures:.......>
    в self информация о сериализаторе  и много чего другого
    Короче если просто писать self без второго атрибута эта штука не работает
    можно написать t1, t2 тогда в первый аргумент все равно вернет self, во второй объект курса название и описание 

    в t1 - Value
    CourseDetailSerializer(<Course: Проектирование месторождений газа нефти: Курс рассматривает базовые принципы проектирования месторождений нефти и газа>, context={'request': <rest_framework.request.Request: GET '/lms/1/'>, 'format': None, 'view': <lms.views.CourseViewSet object>}):
    name = CharField(help_text='введите название курса', label='Название курса', max_length=100)
    description = CharField(allow_blank=True, allow_null=True, help_text='введите описание курса', label='Описание курса', required=False, style={'base_template': 'textarea.html'})
    owner = PrimaryKeyRelatedField(allow_null=True, label='Владелец курса', queryset=User.objects.all(), required=False)
    course_count = SerializerMethodField()
    lesson_count = SerializerMethodField()
    
    в t2 - Value
    <Course: Проектирование месторождений газа нефти: Курс рассматривает базовые принципы проектирования месторождений нефти и газа>
    
    вывод какой, то что в t1 b t2 приходит это касается только модели Course
    В общем возвращаются сложные объекты, которые можно рассмотреть на точке останова, ключающих много разных полей

    """
    def get_lessons(t1, t2):
        my_result =list(Lesson.objects.all().filter(course=t2))
        my_list = []
        for item in my_result:
            my_list.append(item.lesson_name)
        return my_list



    class Meta:
        model = Course
        fields = ("name", "description", "owner", "course_count", "lessons", "lesson_count") #  , "lesson" "courses_info" После описания можно добавить сюда поле , "lesson_count"
