from django.db import models
from test_info.models import Question, Answer, Test, TestDelegation, QuestBlock, TestQuestBlock


class PollQuestion(Question):
    """Модель вопроса в Test360"""

    with_answer_option = models.BooleanField(default=False,
                                             verbose_name="С вариантами ответа")


class PollAnswer(Answer):
    """Модель ответа на вопрос в Test360"""

    question = models.ForeignKey(PollQuestion, on_delete=models.CASCADE,
                                 related_name="answers",
                                 verbose_name="Ответ на вопрос")

    profile = models.ForeignKey('profiles.Profile', on_delete=models.PROTECT,
                                related_name="answers",
                                verbose_name="Сотрудник, давший ответ")


class Poll(Test):
    """Модель составленного Test360"""

    profile = models.ForeignKey('profiles.Profile', on_delete=models.PROTECT,
                                related_name="polls",
                                verbose_name="Для сотрудника")  # Сотрудник, для оценки которого создается Test360

    questions = models.ManyToManyField(PollQuestion, related_name="polls",
                                       verbose_name="Вопросы в опросе")


class PollDelegation(TestDelegation):
    """Модель Test360, назначенного сотрудникам"""

    poll = models.ForeignKey(Poll, on_delete=models.PROTECT,
                             related_name="poll_delegations",
                             verbose_name="Опрос")


class PollQuestBlock(QuestBlock):
    """Модель блока с вопросами для Test360"""

    questions = models.ManyToManyField(PollQuestion, related_name="blocks",
                                       verbose_name="Вопросы в блоке")

    def count_questions(self):
        """Количество вопросов в блока"""
        return self.questions.count()


class PollTestQuestBlock(TestQuestBlock):
    """Модель для связи Test360 и блоков с вопросами"""

    poll = models.ForeignKey(
        Poll,
        on_delete=models.PROTECT,
        related_name="test",
        verbose_name="Тест",
        to_field='id'
    )

    blocks = models.ForeignKey(
        PollQuestBlock,
        on_delete=models.PROTECT,
        related_name="blocks",
        verbose_name="Блоки с вопросами",
        to_field='id'
    )
