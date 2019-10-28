"""assessment1 URL Configuration
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('profiles.urls')),
    path('login/', include('authorization.urls')),
    url(r'^logout$', RedirectView.as_view(url='/login/logout')),
    path('tests/', include('skilltests.urls')),
    path('test360/', include('test360.urls'))
]
