from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.db import models
from django.utils import timezone

from assessment.settings import USERNAME_MAX_LENGTH, USER_CREDENTIALS_MAX_LENGTH, \
    USER_MOBILE_NUMBER_MAX_LENGTH, USER_OCCUPATION_TITLE_MAX_LENGTH, \
    RETURN_STR_LENGTH

ROLE_CHOICES = (
    (1, 'Employee'),
    (2, 'Testmaster'),
    (3, 'Hr'),
    (4, 'Super')
)


class Profile(AbstractUser):
    """Модель профиля пользователя"""

    email_validator = EmailValidator()
    username = models.CharField(
        'E-Mail',
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        help_text='Обязательно. Макс. 300 символов. '
                  'Должен быть корректным E-Mail-адресом.',
        validators=[email_validator],
        error_messages={
            'unique': "Пользователь с таким E-Mail уже существует.",
        },
    )
    # email = username

    first_name = models.CharField(max_length=USER_CREDENTIALS_MAX_LENGTH, blank=False,
                                  verbose_name='Имя')
    middle_name = models.CharField(max_length=USER_CREDENTIALS_MAX_LENGTH, blank=True,
                                   verbose_name='Отчество', null=True)
    last_name = models.CharField(max_length=USER_CREDENTIALS_MAX_LENGTH, blank=False,
                                 verbose_name='Фамилия')
    date_of_birth = models.DateField(verbose_name='Дата рождения',
                                     default=timezone.now)
    # У каждого человека есть
    # официальная дата рождения

    # сменить на ссылку на роль или добавить возможные значения
    role = models.IntegerField(verbose_name='Роль в системе',
                               choices=ROLE_CHOICES, default=1)

    occupation = models.ForeignKey('profiles.Occupation',
                                   on_delete=models.SET_NULL, blank=True,
                                   null=True, related_name='workers',
                                   verbose_name='Должность')
    phone = models.CharField(max_length=USER_MOBILE_NUMBER_MAX_LENGTH, blank=False, null=True,
                             verbose_name='Телефон')

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    '''
    человек не всегда хочет, чтобы все знали его номер телефона. Вопрос безопасности.
    Если HR'у понадобится номер телефона, он может узнать его у тимлида.
    '''

    def __str__(self):
        return f"{self.get_full_name()} ({self.date_of_birth})"

    def get_full_name(self):
        full_name = ' '.join((self.first_name,
                              self.middle_name or '',
                              self.last_name))
        return full_name.replace('  ', ' ')

    get_full_name.short_description = 'Полное имя'

    def new_tests(self):
        """Список непройденных тестов"""

        return self.user_results.filter(result__isnull=True)

    def completed_tests(self):
        """Список пройденных тестов"""
        return self.skilltests_delegations.filter(results__isnull=False)

    def save(self, *args, **kwargs):
        """Сохранение нового пользователя в базу данных"""

        if self.username and not self.email:
            self.email = self.username

        if self.email and not self.username:
            self.username = self.email

        super().save(*args, **kwargs)

    def new_tests360(self):
        """Список непройденных 360 тестов"""

        return self.test360_delegations.filter(profiles__answers__answer__isnull=True)


class Occupation(models.Model):
    """Модель должности пользователя"""

    title = models.CharField(max_length=USER_OCCUPATION_TITLE_MAX_LENGTH, verbose_name='Наименование')
    parent = models.ForeignKey('profiles.Occupation', on_delete=models.SET_NULL,
                               null=True, blank=True,
                               verbose_name='Родительская должность')

    def __str__(self):
        return self.title[:RETURN_STR_LENGTH]

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'
