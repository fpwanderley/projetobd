from django.conf.urls import url

from .views import home, user_login, user_logout, user_checkin

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^login/', user_login, name='login'),
    url(r'^login/(?P<next>.*)$', user_login, name='login'),
    url(r'^home/$', home, name='home'),
    url(r'^checkin/$', user_checkin, name='checkout'),
    url(r'^logout/$', user_logout, name='logout'),
]

