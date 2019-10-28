from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from profiles.models import Profile
from skilltests.models import SkillTest, SkillTestDelegation, SkillTestDelegationResult
import logging

log = logging.getLogger('django')


@login_required(login_url='/login/')
def profile_page(request):
    """Рендеринг страницы с информацией о пользователе и его тестами"""

    log.debug(f'render profile view called with method {request.method}')

    user = request.user

    log.info(f'{user.get_full_name()}: collect tests...')
    delegations = SkillTestDelegationResult.objects.filter(result__isnull=False, profile=user)
    return render(request, 'profiles/profile.html',
                  {
                      "user": user,
                      "tests": delegations,
                  })


def role_required(role_name):
    """Проверка на членство пользователя хотя бы в одной из входных групп"""
    log.debug('check has any role function called with method role_required')

    def has_role(user):
        log.info(f'{user.get_full_name()}: check authentication...')
        if user.is_authenticated():
            log.info(f'{user.get_full_name()}: collect profile data...')
            profile = Profile.objects.get(user=user)
            log.info(f'{user.get_full_name()}: check role...')
            if profile.role == role_name:
                log.info(f'{user.get_full_name()}: has role{role_name}...')
                return True
        log.info(f'{user.get_full_name()}: has not role{role_name}...')
        return False

    return user_passes_test(has_role)
