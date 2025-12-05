import re
from rest_framework.serializers import ValidationError


class YouTubeValidator:
    """ Валидатор для проверки ссылки на видео.
    Разрешает только ссылки с youtube.com """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reg = re.compile(r'^https://www.youtube.com/')
        tmp_val = dict(value).get(self.field)

        if not tmp_val:
            return

        if 'youtube.com' not in tmp_val:
            raise ValidationError('Ссылка на видео должна быть только с youtube.com')
