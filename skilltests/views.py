from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, SuspiciousOperation
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views import View
import logging

from skilltests.models import SkillTestAnswer, SkillTestDelegation, SkillTestQuestBlock, SkillTestDelegationResult

log = logging.getLogger('django')


class TestPage(View):
    """Рендеринг страницы с тестом для пользователя"""

    http_method_names = ['get', 'post']

    def get_delegation_attributes(self, pk):
        log.info('start method get_delegation_attributes and collect data...')
        self.delegation = get_object_or_404(SkillTestDelegation, id=pk)
        self.test = self.delegation.test

        blocks = SkillTestQuestBlock.objects.filter(test=self.test)
        for block in blocks:
            block_questions = block.block.questions.order_by('?')[
                              :block.count_questions]  # получаем случайные вопросы в заданном количестве
            self.blocks.append((block.block.title, block_questions))
            for question in block_questions:
                self.test.questions.add(question)
        self.test.save()
        log.info('end method get_delegation_attributes and data was collected...')

    def __init__(self, **kwargs):
        log.info('Starter constructor of TestPage(View)...')
        super().__init__(**kwargs)
        self.delegation = None
        self.test = None
        self.blocks = []
        self.result = None

    def get(self, request, pk):
        log.debug('start http method get and collect data...')
        user = request.user
        self.get_delegation_attributes(pk)

        self.result = SkillTestDelegationResult.objects.get(profile=user)

        # if self.delegation.profiles != user:
        #     return HttpResponse(status=401)

        log.info('start timer...')
        self.result.start_time = timezone.now()
        self.result.save()

        log.debug('render test_page...')
        return render(request,
                      'skilltests/test_page.html',
                      {
                          "user": user,
                          "test": self.test,
                          "blocks": self.blocks
                      })

    def post(self, request, pk):
        log.debug('start http method post and collect data...')

        self.get_delegation_attributes(pk)
        print(self.result)
        self.result = SkillTestDelegationResult.objects.get(profile=request.user)
        self.result.end_time = timezone.now()
        correct_answers = 0

        log.info('start collect correct answers...')
        for question in self.test.questions.all():
            try:
                if question.is_few_right_answers:
                    log.info('check for few correct answers...')
                    correct_answers += self.get_points_for_multiple_answer(request, question)
                else:
                    log.info('check for one correct answers...')
                    correct_answers += self.get_points_for_single_answer(request, question)
            except KeyError:
                log.warning('KeyError on collecting right answers!!!')
                return HttpResponse(status=400)

        log.info('count the result...')
        self.result.result = correct_answers / len(self.test.questions.all())
        self.result.save()

        return redirect('test_finish', pk=self.delegation.pk)

    def get_points_for_multiple_answer(self, request, question):
        log.debug(f'count points for mult ans called with method: {request.method}')
        selected_ids = request.POST.getlist(str(question.pk) + '[]')
        correct_answers = question.answers.filter(right=True)
        point = 1
        if len(selected_ids) == correct_answers.count():
            log.info(f'len of correct ans not equal selected ans, checked be method: {request.method}')
            log.debug(f'end count points for mult ans called with method: {request.method}')

            for answer_id in selected_ids:
                if SkillTestAnswer.objects.get(id=answer_id) not in correct_answers:
                    log.info(f'answer is not correct, checked be method {request.method}')
                    log.debug(f'end count points for mult ans called with method: {request.method}')
                    point = 0
                    break
            log.debug(f'end count points for mult ans called with method: {request.method}')

        else:
            point = 0

        return point

    def get_points_for_single_answer(self, request, question):
        log.debug(f'count points for single ans called with method: {request.method}')
        answer_id = request.POST[str(question.pk)]

        try:
            selected = SkillTestAnswer.objects.get(id=answer_id)
        except ObjectDoesNotExist:
            log.warning(f'Object does not exist in method: {request.method}')
            raise SuspiciousOperation("SkillTestAnswer {}  does not exists.".format(answer_id))

        point = 0
        if selected.right:
            point = 1
        log.debug(f'end count points for single ans called with method: {request.method}')
        return point


@login_required
def test_list(request):
    """Рендеринг страницы со всеми непройденными тестами, назначенными сотруднику"""
    log.debug(f'rendering all test for emploee with method: {request.method}')

    user = request.user
    log.info(f'get all tests for {user.get_full_name()}')
    delegations = SkillTestDelegationResult.objects.filter(profile=user, result__isnull=True)
    log.debug(f'end rendering all test for emploee with method: {request.method}')
    return render(request,
                  'skilltests/test_list.html',
                  {
                      "user": user,
                      "delegations": delegations,
                  })


@login_required
def test_finish(request, pk):
    """Рендеринг страницы с результатом пройденного сотрудником теста"""
    log.debug(f'rendering result of test for emploee with method: {request.method}')

    user = request.user
    delegation = get_object_or_404(SkillTestDelegation, id=pk)
    delegation_result = get_object_or_404(SkillTestDelegationResult, profile=user, skill_test_delegation=delegation)
    if delegation_result.result is None:
        return redirect('test_page', pk=pk)

    # код ниже, скорее, уже не нужен, тк сейчас один тест может делегироваться нескольким профилям
    # if delegation.profile != user:
    #     return HttpResponse(status=401)
    test = delegation_result.skill_test_delegation.test

    log.debug(f' end rendering result of test for emploee with method: {request.method}')
    return render(request,
                  'skilltests/test_finish.html',
                  {
                      "user": user,
                      "delegation": delegation_result,
                      "test": test
                  })
