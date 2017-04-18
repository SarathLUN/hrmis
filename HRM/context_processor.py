__author__ = 'Tusfiqur'
from attendance.models import AttendanceHistory
from account.models import EmployeeUser,GroupTable,MenuTable,MenuGroupTable,UserGroupTable
from hr.models import EmployeeDesignation
from django.template import context
from datetime import date,datetime
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from attendance.attendance_module_functions import get_entry_time,get_attendance_status, get_endorsement_status
from leave.models import LeaveHistory
from attendance.models import Late


menu_string = ""


def get_login_time(request):
    t='222'
    #print(request.user.id)
    try:
        v = EmployeeUser.objects.get(user_id=request.user.id)
        emp_des_obj = EmployeeDesignation.objects.get(employee_id=v.employee.employee_id, isActive=True)
        login_time = get_entry_time(v.employee.cardId, date.today())
        #get_last_data_time = get_entry_time(v.employee.cardId)
        if login_time != 'N/A':
            t = datetime.strptime(login_time, '%H:%M:%S')
            #print(t.date())
            attendance_status = get_attendance_status(t,date.today(), emp_des_obj.location_id.location_id)
            endorsement_status = get_endorsement_status(v.employee.employee_id, date.today())
            #print(endorsement_status)
        else:
            t = 'N/A'
            attendance_status = 'N/A'
            endorsement_status = 'N/A'

        subordinate_list = EmployeeDesignation.objects.filter(isActive=True, supervisor=emp_des_obj.employee_id).values('employee_id')

        pending_application_list_count = LeaveHistory.objects.filter(endorsed_by = request.user.employeeuser.employee, endorsement='0', isActive=True).order_by('-insertDate')

        message_list = Late.objects.filter(isActive=True, isEndorsed='0', emp_id_id__in=subordinate_list).order_by('-date')

    except ObjectDoesNotExist:
        login_time = 'no'
        attendance_status = 'N/A'
        endorsement_status = 'N/A'
        message_list = -1
        pending_application_list_count = -1

    except MultipleObjectsReturned:
        login_time = 'no'
        attendance_status = 'N/A'
        endorsement_status = 'N/A'
        message_list = -1
        pending_application_list_count = -1

    return {'login_time' : t,
            'attendance_status' : attendance_status,
            'endorsement_status' : endorsement_status,
            'message_count' : message_list,
            'leave_approval_count' : pending_application_list_count
            }


def get_menu_table(request):

    str = "/leave/add/applyLeave/"
    global menu_string
    menu_string = ''
    try:
        v = EmployeeUser.objects.get(user_id=request.user.id)
        get_user_group = UserGroupTable.objects.get(user_id=v)
        get_menu_list = MenuGroupTable.objects.filter(menu_group_id=get_user_group.group_id)

        for list in get_menu_list:

            if list.menu_id.parent_id_id is None:
                generate_menu(list.menu_id,get_user_group)
    except:
        menu_string = ''

    return {'menu_string' : menu_string}


def generate_menu(list,user_group):

    global menu_string
    if list.has_child:

        menu_string = menu_string + '<li class="xn-openable"><a href="#"><span class="fa fa-sitemap"></span> <span class="xn-text">' + list.menu_string + '</span></a><ul>'
        get_child_list = MenuTable.objects.filter(parent_id=list)
        for child_list in get_child_list:
            if MenuGroupTable.objects.filter(menu_group_id=user_group.group_id, menu_id=child_list.id).exists():
                generate_menu(child_list,user_group)

        menu_string = menu_string + '</ul></li>'


    else:
        menu_string = menu_string + '<li class=""> <a href=' + list.url_string + '><span class="fa fa-desktop"></span>' + list.menu_string + '</a></li>'

#def get_last_data_entry_time(card_id):

#    attendance_history = AttendanceHistory.objects.filter(emp_card_id=card_id).latest()

# def get_notification(request):
#
#     try:
#         pending_application_list_count = LeaveHistory.objects.filter(endorsed_by = request.user.employeeuser.employee, endorsement='0', isActive=True).count()
#     except:
#         pending_application_list_count = -1
#
#
#     return {'leave_approval_count' : pending_application_list_count}

