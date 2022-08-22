from django.conf.urls import url
from django.contrib.auth.views import login
from . import views


urlpatterns = [
    url(r'register/$', views.register, name='register'),
    url(r'login/$', login, {'template_name': 'reg_and_login.html'}, name='login'),
    url(r'logout/$', views.logout_view, name='logout'),
    url(r'ranking/$', views.ranking, name='ranking')
]