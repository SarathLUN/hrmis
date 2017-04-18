__author__ = 'Tusfiqur'
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^password_change/$',views.password_change, name='password_change'),
    url(r'^create_user/$', views.create_employee_user, name='create_employee_user'),
    url(r'^add_menu/$', views.add_new_menu, name='add_new_menu'),
    url(r'^user_group/$', views.add_user_group, name='add_new_group'),
    url(r'^user_calender/$', views.user_calender, name='user_calender'),
]