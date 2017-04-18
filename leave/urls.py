__author__ = 'Tusfiqur'
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^(?P<message>[A-Za-z]+)/addLeaveCategory/$', views.addLeaveCategoryPage, name="addLeaveCategoryPage"),
    url(r'^addLeaveCategoryPerfomed/$', views.addLeaveCategoryPerfomed, name="addLeaveCategoryPerfomed"),
    url(r'^(?P<category_id>[0-9]+)/editLeaveCategory/$', views.editLeaveCategoryPage, name="editLeaveCategory"),
    url(r'^(?P<message>[A-Za-z]+)/applyLeave/$', views.applyLeave, name="applyLeave"),
    url(r'^pendingApplication/$', views.pendingApplication, name="pendingApplication"),
    url(r'^(?P<leave_id>[0-9]+)/(?P<status>[a-z]+)/approval/$', views.applicationApproval, name="applicationApproval"),
    url(r'^admin_leave_page/$', views.admin_leave_page, name="admin_leave_page"),
    url(r'^admin_approval_modification/$', views.admin_approval_modification, name="admin_approval_modification"),
    url(r'^(?P<leave_id>[0-9]+)/(?P<request_type>[a-z]+)/adminEditLeave/$', views.admin_leave_edit, name="admin_leave_req_edit"),
    url(r'^(?P<sms_id>[0-9]+)/(?P<request_type>[a-z]+)/adminEditSms/$', views.admin_attendance_sms_edit, name="admin_sms_attendance_edit"),
    url(r'^(?P<leave_id>[0-9]+)/leave_print/$', views.leave_print, name="print_leave"),
]