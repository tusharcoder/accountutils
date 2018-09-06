# @Author: Tushar(tusharcoder) <tushar>
# @Date:   05/09/18
# @Email:  tamyworld@gmail.com
# @Filename: urls
# @Last modified by:   Tushar

from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^request/forgot/password/$', forgot_password_view, name='request_forgot_password'),
    url(r'^check/forgot_password_code/$', forgot_password_confirm, name='check_forgot_password_code'),
    url(r'^reset/password/$', reset_password, name='reset_password'),
    url(r'^change/password/$', change_password, name='change_password'),
    # url(r'^login/$', login, name='login'),
]
