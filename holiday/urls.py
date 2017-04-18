__author__ = 'Tusfiqur'

from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^addWeeklyHoliday/$', views.addWeeklyHoliday, name="addWeeklyHoliday"),
    url(r'^addWeeklyHolidayPerfomed/$', views.addWeeklyHolidayPerfomed, name="addWeeklyHolidayPerfomed"),
    url(r'^addYearlyHoliday/$', views.addYearlyHoliday, name="addYearlyHoliday"),
    url(r'^addYearlyHolidayPerfomed/$', views.addYearlyHolidayPerfomed, name="addYearlyHolidayPerfomed"),
    url(r'^(?P<flag_id>[0-9]+)/editYearlyHolidayPerfomed/$', views.editYearlyHolidayPerfomed, name="editYearlyHolidayPerfomed"),
]