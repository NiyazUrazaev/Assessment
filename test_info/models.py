from django.db import models
from assessment.settings import RETURN_STR_LENGTH, TITLE_MAX_LENGTH


class Question(models.Model):
    """Модель вопроса в тесте"""

    title = models.TextField(verbose_name="Текст вопроса")

    def __str__(self):
        return self.title[:RETURN_STR_LENGTH] + '...'

    class Meta:
        abstract = True
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    """Модель ответа на вопрос в тесте"""

    answer = models.TextField(verbose_name="Текст ответа", null=True,
                              blank=True)

    def __str__(self):
        return self.answer[:RETURN_STR_LENGTH] + '...'

    class Meta:
        abstract = True
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class Test(models.Model):
    """Модель составленного теста"""

    title = models.CharField(max_length=TITLE_MAX_LENGTH, verbose_name="Название")

    def __str__(self):
        return self.title[:RETURN_STR_LENGTH] + '...'

    class Meta:
        abstract = True
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class TestDelegation(models.Model):
    """Модель теста, назначенного сотруднику"""

    profiles = models.ManyToManyField('profiles.Profile',
                                      related_name='%(app_label)s_delegations',
                                      verbose_name="Сотрудники")

    class Meta:
        abstract = True
        verbose_name = 'Назначение теста'
        verbose_name_plural = 'Назначения тестов'


class QuestBlock(models.Model):
    """Модель блока с вопросами для теста"""

    title = models.CharField(max_length=TITLE_MAX_LENGTH, verbose_name="Название")

    def __str__(self):
        return self.title[:RETURN_STR_LENGTH] + '...'

    class Meta:
        abstract = True
        verbose_name = 'Блок вопросов'
        verbose_name_plural = 'Блоки вопросов'


class TestQuestBlock(models.Model):
    """Модель для связи Тестов и Блоков"""

    class Meta:
        abstract = True
