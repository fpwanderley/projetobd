from django.conf.urls import url

from .views import home, login, prelogin


urlpatterns = [
    url(r'^$', prelogin, name='prelogin'),
    url(r'^login/$', login, name='login'),
    url(r'^home/$', home, name='home'),
]
