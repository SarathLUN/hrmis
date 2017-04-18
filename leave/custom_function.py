__author__ = 'Tusfiqur'
from hr.models import EmployeeDesignation, Employee
from .models import LeaveCategory, LeaveAllotment
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime,timedelta
from . import views

def get_leave_balance(EmployeeDesignation, Employee):

    leaveCategory_obj_list = LeaveCategory.objects.filter(isActive=True)
    leave_balance_list = []

    policy = True

    for category in leaveCategory_obj_list:
        allocated_balance = category.amount

        try:
            leave_balance = LeaveAllotment.objects.get(leave_id__type__id = category.id, isActive=True, employee_id=EmployeeDesignation.employee_id)
            leave_balance_list.append({'id' : category.id, 'name' : category.name, 'balance' : leave_balance.balance})

        except ObjectDoesNotExist:
            leave_balance_list.append({'id' : category.id, 'name' : category.name, 'balance' : category.amount})

    return leave_balance_list
