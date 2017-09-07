__author__ = 'Tusfiqur'

from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^showAttedanceList/$', views.showAttendanceList, name="showAttedanceList"),
    url(r'^(?P<message_id>[a-zA-Z]+)/addRegularOfficeTime/$', views.addRegularOfficeTime, name="addRegularOfficeTime"),
    url(r'^addException/$', views.addExceptionOfficeTime, name="addExceptionOfficeTime"),
    url(r'^lateAttendance/$',views.lateAttendance, name="lateAttendance"),
    url(r'^getEmployeeAttendanceHistory/$', views.getEmployeeAttendaceHistory, name="getEmployeeAttendace"),
    url(r'^(?P<late_id>[0-9]+)/(?P<choice>[a-z]+)/lateEndorsement/$', views.lateEndorsement, name="lateAttendanceEndorsement"),
    url(r'^readsms/$', views.readSms, name="readsms"),
    url(r'^generateSms/$', views.generate_sms_to_late, name='generate_sms'),
    url(r'^(?P<sms_id>[0-9]+)/deleteSms/$', views.deleteSms, name='delete_sms'),
    url(r'^getUserAttendance/$', views.get_own_attendance, name='get_own_attendance'),
    url(r'^absentReport/$', views.absent_report, name='absent_report'),
    url(r'^employeeAbsentReport/$', views.employee_absent_report, name='employee_absent_report'),
    url(r'^movementReprot/$', views.movement_report, name='movement_report'),
    url(r'^userSmsList/$', views.view_user_sms, name='user_sms_list'),
    url(r'^reportSetting/$', views.attedance_report_setting, name="report_setting"),
    url(r'^setParentChild/$', views.attedance_report_setting, name="set_parent_child"),
    url(r'(?P<parent_id>[0-9]+)/create_relation/$', views.parent_child_relation, name="create_relation"),
    url(r'endorsementReport/$', views.endorsement_report, name="endorsement_report"),
    url(r'dailyAttendance/$', views.dailyAttendaceReport, name="daily_attendance"),
]