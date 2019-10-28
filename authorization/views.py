import logging

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import auth

log = logging.getLogger('django')


def login(request):
    """'Аутентификация пользователя"""

    if request.user.is_authenticated:
        return redirect('profile')

    log.debug(f'login view called with method {request.method}')

    if request.POST:
        email = request.POST['email']
        password = request.POST['password']

        log.info(f'{email}: authenticating...')
        user = auth.authenticate(username=email, password=password)

        if user:
            log.info(f'{email}: logging in...')
            auth.login(request, user)
            log.info(f'{email}: logged in')

            return redirect('profile')
        else:
            log.info(f'{email}: login failed')
            return render(request,
                          'authorization/login.html',
                          {'error': 'Неверный пароль'})

    return render(request, 'authorization/login.html')


def logout(request):
    """Отмена авторизации пользователя"""

    log.debug(f'logout view called with method {request.method}')

    email = request.user.username

    log.info(f'{email}: logging out...')
    auth.logout(request)
    log.info(f'{email}: logged out')
    return redirect('login')
