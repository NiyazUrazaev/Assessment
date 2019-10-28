from django.urls import path
from . import views

urlpatterns = [
    path('', views.test_list, name='test_list'),
    path('<int:pk>', views.TestPage.as_view(), name='test_page'),
    path('<int:pk>/finish', views.test_finish, name='test_finish')
]
