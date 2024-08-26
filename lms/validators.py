from rest_framework import serializers


class YoutubeValidators:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        # В value закидывается вообще весь объект с полями lesson_name, 'lesson_url', объект 'course' value['lesson_url']
        val = dict(value).get(self.field)
        # Поле self.fild у нас это 'lesson_url', вся строка возвращает ссылку на адрес на ютуб
        # Ниже начинается проверка уже переменной val в которой находится ссылка
        if val and "youtube.com" not in val:
            raise serializers.ValidationError(f"{self.field} должен ссылаться только на видео с youtube.com")
