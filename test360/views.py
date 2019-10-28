import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from test360.models import PollDelegation, PollAnswer

log = logging.getLogger('django')


@login_required
def test_finish(request, pk):
    log.debug(f'rendering finish of test360 with method: {request.method}')
    """Рендеринг страницы с результатом пройденного сотрудником теста 360"""

    log.info(f'get user and delegation in method {request.method}')
    user = request.user
    delegation = get_object_or_404(PollDelegation, id=pk)

    log.info(f'checking equals of user and delegation in method {request.method}')
    if user not in delegation.profiles.all():
        log.warning(f'this delegation is not for this user ex 401 in method {request.method}')
        return HttpResponse(status=401)
    poll = delegation.poll

    log.debug(f'end rendering finish of test360 with method: {request.method}')
    return render(request,
                  'test360/test_finish.html',
                  {
                      "user": user,
                      "delegation": delegation,
                      "test": poll
                  })


@login_required
def test_list(request):
    """Рендеринг страницы со всеми непройденными  360 тестами, назначенными сотруднику"""
    log.debug(f'rendering all tests 360 with method: {request.method}')

    log.info(f'get user and delegation for him in method {request.method}')
    user = request.user
    delegations = PollDelegation.objects.filter(profiles=user,
                                                profiles__answers__answer__isnull=True)

    log.debug(f'end rendering finish of test360 with method: {request.method}')
    return render(request,
                  'test360/test_list.html',
                  {
                      "user": user,
                      "delegations": delegations,
                  })


@login_required
def test_questions(request, pk):
    log.debug(f'get questions of test 360 with method: {request.method}')
    log.info(f'get questions of test 360 from delegation with method: {request.method}')
    poll_delegation = get_object_or_404(PollDelegation, id=pk)
    questions = poll_delegation.poll.questions.all()
    response = render(request, 'test360/test_questions.html', {'questions': questions})
    if request.POST:
        for question in questions:
            if str(question.pk) in request.POST:
                answer = PollAnswer(
                    answer=request.POST[str(question.pk)],
                    profile=request.user,
                    question=question
                )
                answer.save()
        response = redirect("test_finish360", pk=pk)
    log.debug(f'end get questions of test 360 with method: {request.method}')
    return response
