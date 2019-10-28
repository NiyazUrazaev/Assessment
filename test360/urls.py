from django.urls import path

from test360 import views

urlpatterns = [
    path('', views.test_list, name="test_list360"),
    path('<int:pk>/finish', views.test_finish, name='test_finish360'),
    path('<int:pk>', views.test_questions, name='test360_questions')
]