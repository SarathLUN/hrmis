__author__ = 'Tusfiqur'
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^(?P<message>[A-Za-z]+)/addEmployee/$', views.addEmployeePage, name="addEmployeePage"),
    url(r'^addEmployeePerfomed/$', views.addEmployeePerfomed, name="addEmployeePerfomed"),
    url(r'^(?P<message>[A-Za-z]+)/employeeList/$', views.viewEmployeeList, name="viewEmployeeList"),
    url(r'^(?P<employee_id>[0-9]+)/editEmployee/$', views.editEmployee, name="editEmployee"),
    url(r'^(?P<employee_id>[0-9]+)/editEmployeePerfomed/$', views.editEmployeePerfomed, name="editEmployeePerfomed"),
    url(r'^(?P<message>[A-Za-z]+)/addDepartment/$', views.addDepartmentPage, name="addDepartmentPage"),
    url(r'^addDepartmentPerfomed/$', views.addDepartmentPerfomed, name="addDepartmentPerfomed"),
    url(r'^(?P<dept_id>[0-9]+)/departmentEdit/$', views.editDepartmentPerformed, name="editDepartmentPerfomed"),
    url(r'^(?P<message>[A-Za-z]+)/addDesignation/$', views.addDesignation, name="addDesignationPage"),
    url(r'^addDesignationPerfomed/$', views.addDesingationPerfomed, name="addDesignationPerfomed"),
    url(r'^(?P<des_id>[0-9]+)/designationEdit/$', views.editDesignationPerfomed, name="editDesignationPerfomed"),
    url(r'^(?P<message>[A-Za-z]+)/addLocation/$', views.addLocationPage, name="addLocationPage"),
    url(r'^addLocationPerfomed/$', views.addLocationPerfomed, name="addLocationPerfomed"),
    url(r'^(?P<loc_id>[0-9]+)/locationEdit/$', views.editLocationPerfomed, name="editLocationPerfomed"),
    url(r'^addEmployeeDesignation/$', views.addEmployeeDesignationPage, name="addEmployeeDesignationPage"),
    url(r'^addEmployeeDesignationPerfomed/$', views.addEmployeeDesignationPerfomed, name="addEmployeeDesignantionPerfomed"),
    url(r'^(?P<emp_des_id>[0-9]+)/editEmployeeDesignation/$', views.editEmployeeDesignationPerfomed, name="editEmployeeDesignationPerfomed"),
    url(r'^editEmployeeDesignationPage_admin/$', views.editEmployeeDesignation_admin, name="editEmployeeDesignationPage"),
    url(r'^(?P<emp_des_id>[0-9]+)/editEmployeeDesignation_admin/$', views.editEmployee_admin, name="editEmployeeDesignationAdmin"),
]
