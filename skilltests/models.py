from django.db import models
from test_info.models import Question, Answer, Test, TestDelegation, QuestBlock, TestQuestBlock


class SkillTestQuestion(Question):
    """Модель вопроса в SkillTest"""

    is_few_right_answers = models.BooleanField(default=False,
                                verbose_name="Несколько вариантов ответа?")

    code = models.TextField(verbose_name="Кусок кода", null=True, blank=True)


class SkillTestAnswer(Answer):
    """Модель ответа на вопрос в SkillTest"""

    code = models.TextField(verbose_name='Кусок кода', null=True, blank=True)

    question = models.ForeignKey(SkillTestQuestion, on_delete=models.CASCADE,
                                 related_name="answers",
                                 verbose_name="На вопрос")

    right = models.BooleanField(default=False, verbose_name="Правильный?")


class SkillTest(Test):
    """Модель составленного SkillTest"""

    blocks = models.ManyToManyField('SkillQuestBlock',
                                    related_name="tests",
                                    verbose_name="Блоки с вопросами",
                                    through='SkillTestQuestBlock')

    count_of_quest = models.IntegerField(default=0,
                                    verbose_name='Количество вопросов в тесте')

    questions = models.ManyToManyField('SkillTestQuestion',
                                       related_name="tests",
                                       verbose_name="Все вопросы теста")

    # def get_questions(self):
    #     tests = SkillTestQuestBlock.objects.prefetch_related().filter(test=self)
    #     dict_blocks = {}
    #     for test in tests:
    #         questions = list(test.blocks.questions.all())
    #         random_questions = random.sample(questions, k=test.count_questions)
    #         dict_blocks.update({test.blocks: random_questions})
    #     return dict_blocks


class SkillTestDelegation(TestDelegation):
    """Модель SkillTest-a, назначенного сотруднику"""

    test = models.ForeignKey(SkillTest, on_delete=models.PROTECT,
                             related_name="delegations",
                             verbose_name="Тест")
    profiles = models.ManyToManyField('profiles.Profile',
                                      through='skilltests.SkillTestDelegationResult',
                                      related_name='%(app_label)s_delegations',
                                      verbose_name="Сотрудники")


class SkillTestDelegationResult(models.Model):
    skill_test_delegation = models.ForeignKey(SkillTestDelegation,
                                              related_name='results',
                                              on_delete=models.SET_NULL,
                                              null=True,
                                              verbose_name='Назначение')
    profile = models.ForeignKey('profiles.Profile',
                                related_name='user_results',
                                on_delete=models.SET_NULL,
                                null=True,
                                verbose_name='Человек, которому назначили тест')

    result = models.FloatField(verbose_name="Результат", null=True, blank=True)
    start_time = models.DateTimeField(verbose_name="Время начала прохождения",
                                      null=True, blank=True)
    end_time = models.DateTimeField(verbose_name="Время конца прохождения",
                                    null=True, blank=True)

    def duration(self):
        """Время, которое было потрачено сотрудником на прохождение SkillTest"""

        if self.end_time and self.start_time:
            return self.end_time - self.start_time
        return None


class SkillQuestBlock(QuestBlock):
    """Модель блока с вопросами для SkillTest-a"""

    questions = models.ManyToManyField(SkillTestQuestion, related_name="blocks",
                                       verbose_name="Вопросы в блоке")

    def count_questions(self):
        """Количество вопросов в блоке"""
        return self.questions.count()


class SkillTestQuestBlock(TestQuestBlock):
    """Модель для связи SkillTest-ов и блоков с вопросами"""

    test = models.ForeignKey(
        SkillTest,
        on_delete=models.PROTECT,
        related_name="test",
        verbose_name="Тест",
        to_field='id'
    )

    block = models.ForeignKey(
        SkillQuestBlock,
        on_delete=models.PROTECT,
        related_name="block",
        verbose_name="Блок с вопросами, подготовленными специально для теста",
        to_field='id'
    )

    count_questions = models.PositiveSmallIntegerField(
        verbose_name="Количество вопросов из блока")

    def save(self, *args, **kwargs):
        super(SkillTestQuestBlock, self).save(*args, **kwargs)
        amt = 0
        blocks = SkillTestQuestBlock.objects.filter(test=self.test)
        for block in blocks:
            amt += block.count_questions
        self.test.count_of_quest = amt
        self.test.save()
