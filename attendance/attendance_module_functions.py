__author__ = 'Tusfiqur'
from datetime import date,datetime,timedelta
from attendance.models import AttendanceHistory,RegularOfficeTime, Late
from hr.models import Employee,EmployeeDesignation
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from holiday.models import YearlyHoliday, WeeklyHoliday,WeekDays
from leave.models import LeaveDetail, LeaveHistory, LeaveAllotment, LeaveCategory,Employee
from attendance.models import *
from HRM.myScript import convert_to_date
from datetime import datetime,timedelta,date,time
from time import time
from account.models import EmployeeUser

def get_attendance_information(date_value, employee):

    status = "<span class=\"label label-warning\">Present</span>"
    endorsement = ""
    late_message = ''
    in_time = ""
    out_time = ""
    login_limit = "N/A"
    day_status = ''

    working_day = True
    late_status = False

    if YearlyHoliday.objects.filter(date=date_value).exists():

        status = "Holiday"
        in_time = ""
        out_time = ""
        login_limit = "N/A"
        endorsement = ''
        late_message = ""

        working_day = False
        day_status = ''

    elif WeeklyHoliday.objects.filter(effectiveFrom__lte=date_value, effectiveEnd__gte=date_value.date(), dayNum=date_value.isoweekday()).exists():

        status = "Weekend"
        in_time = ""
        out_time = ""
        login_limit = "N/A"
        endorsement = ""
        late_message = ""

        working_day = False

    elif LeaveDetail.objects.filter(date=date_value, leave_id__employee_id=employee.employee_id, leave_id__endorsement='1', isActive=True).exists():

        try:
            leave_obj = LeaveDetail.objects.get(date=date_value, leave_id__employee_id=employee.employee_id, leave_id__endorsement='1', isActive=True)
            leave_label = leave_obj.leave_id.type.name
        except MultipleObjectsReturned:
            leave_label = 'Unrecongnized Leave'

        day_status = 'leave'

        status = "<span class=\"label label-warning\" style='background-color: #1370BF;'>" + leave_label +"</span>"
        in_time = ""
        out_time = ""
        login_limit = "N/A"
        endorsement = ""
        late_message = ""

        working_day = True


    elif LeaveDetail.objects.filter(date=date_value, leave_id__employee_id=employee.employee_id, leave_id__endorsement='0', isActive=True).exists():

        day_status = 'absent'

        status = "<span class=\"label label-danger\">Absent</span>"
        endorsement = "Leave Application Pending"
        in_time = ""
        out_time = ""
        login_limit = "N/A"
        late_message = ""

        working_day = True

    elif (date_value.date() <= date.today()) and working_day == True:


        try:
            office_time = RegularOfficeTime.objects.get(start_effective_date__lte=date_value, end_effective_date__gte=date_value)

            '''
            office_time_value = datetime(100,1,1,office_time.office_start_time.hour, office_time.office_start_time.minute, office_time.office_start_time.second)

            grace_time = office_time.grace_amount
            office_time_with_grace_time = office_time_value + timedelta(minutes=grace_time)
            '''
            office_time_with_grace_time = office_time.entry_time_with_grace
            if office_time.remarks != '':
                endorsement = office_time.remarks


        except ObjectDoesNotExist:
            office_time = RegularOfficeTime.objects.get(start_effective_date__lte=date_value, isActive=True)
            office_time_with_grace_time = office_time.entry_time_with_grace

        try:
            in_out = get_in_out(employee.cardId, date_value)
            emp_in_time = AttendanceHistory.objects.filter(emp_card_id=employee.cardId,
                                                           in_out=in_out,
                                                           date=date_value).order_by('id')[0:1].get()
            in_time = emp_in_time.time
            in_time_value = datetime.strptime(in_time,"%H:%M:%S")
            in_time = in_time_value.strftime("%I:%M %p")
            if in_time_value.time() > office_time_with_grace_time:
                status = "<span class=\"label label-danger\" style='background-color: #D1952C'>Late</span>"
                late_status = True


                if Late.objects.filter(date__contains=datetime.date(date_value), emp_id=employee.employee_id, isEndorsed='1').exists():
                    endorsement = "Endorsed"
                    late_object = Late.objects.filter(date__contains=datetime.date(date_value), emp_id=employee.employee_id, isEndorsed='1')[0]
                    late_message = late_object.sms_text

                else:
                    endorsement = "Not Endorsed"


        except ObjectDoesNotExist:
            in_time = 'N/A'

        try:
            out_in = get_out_in(employee.cardId, date_value)
            emp_out_time = AttendanceHistory.objects.filter(emp_card_id=employee.cardId,
                                                           in_out=out_in,
                                                           date=date_value).order_by('-id')[0:1].get()
            out_time = datetime.strptime(emp_out_time.time, "%H:%M:%S")
            out_time = out_time.strftime("%I:%M %p")

        except ObjectDoesNotExist:
            out_time = 'N/A'

        '''if in_time != 'N/A' and out_time != 'N/A':

            status = "<span class=\"label label-warning\">Present</span>"
            late_message = ""
            login_limit = office_time.office_start_time
        '''
        if in_time == 'N/A' and out_time == 'N/A':
            status = "<span class=\"label label-danger\">Absent</span>"
            endorsement=''
            login_limit = "N/A"
            day_status = 'absent'

        elif (in_time == 'N/A' and out_time != 'N/A'):
            status = "<span class=\"label label-warning\" style='background-color: #42209e;'>I/R</span>"
            day_status = 'ir'

        elif (in_time != 'N/A' and out_time == 'N/A'):
            ''' status = "<span class=\"label label-warning\" style='background-color: #42209e;'>I/R</span>"
            count_ir += 1
            '''
            pass

    return (working_day, status, day_status, in_time, out_time, login_limit, late_message, endorsement, late_status)


'''
    this is the modified function of function get_attendance_information().
    it returns the attendance report at holiday, weekday also
'''
def get_attendance_information_extended(date_value, employee):

    status = "<span class=\"label label-warning\">Present</span>"
    endorsement = ""
    late_message = ''
    in_time = ""
    out_time = ""
    login_limit = "N/A"
    day_status = ''

    working_day = True
    late_status = False
    attendance_in_holiday = False

    if (RegularOfficeTime.objects.filter(start_effective_date__lte=date_value, end_effective_date__gte=date_value, location_id=employee.location_id).exists())==False:

        working_day = "No Device"
        status = "No Device" #it refers no attendance_device at that location
        day_status = 'No Device'
        in_time = "No Device"
        out_time = "No Device"
        login_limit = "N/A"
        late_message = 'No Device'
        endorsement = "No Device"
        late_status = "No Device"
        attendance_in_holiday = "No Device"

        return (working_day, status, day_status, in_time, out_time, login_limit, late_message, endorsement, late_status, attendance_in_holiday)



    if (date_value.date() <= date.today()) and AttendanceHistory.objects.filter(emp_card_id=employee.employee_id.cardId, date=date_value).exists():


        try:
            office_time = RegularOfficeTime.objects.get(start_effective_date__lte=date_value, end_effective_date__gte=date_value, location_id=employee.location_id)

            '''
            office_time_value = datetime(100,1,1,office_time.office_start_time.hour, office_time.office_start_time.minute, office_time.office_start_time.second)

            grace_time = office_time.grace_amount
            office_time_with_grace_time = office_time_value + timedelta(minutes=grace_time)
            '''
            office_time_with_grace_time = office_time.entry_time_with_grace
            if office_time.remarks != '':
                endorsement = office_time.remarks


        except ObjectDoesNotExist:
            office_time = RegularOfficeTime.objects.get(start_effective_date__lte=date_value, isActive=True, location_id=employee.location_id)
            office_time_with_grace_time = office_time.entry_time_with_grace

        try:
            in_out = get_in_out(employee.employee_id.cardId, date_value)
            emp_in_time = AttendanceHistory.objects.filter(emp_card_id=employee.employee_id.cardId,
                                                           in_out=in_out,
                                                           date=date_value).order_by('id')[0:1].get()
            in_time = emp_in_time.time
            in_time_value = datetime.strptime(in_time,"%H:%M:%S")
            in_time = in_time_value.strftime("%I:%M %p")
            if in_time_value.time() > office_time_with_grace_time:
                status = "<span class=\"label label-danger\" style='background-color: #D1952C'>Late</span>"
                late_status = True


                if Late.objects.filter(date__contains=datetime.date(date_value), emp_id=employee.employee_id.employee_id, isEndorsed='1').exists():
                    if endorsement != '':
                        endorsement = "Endorsed" + ' # ' + endorsement
                    else:
                        endorsement = "Endorsed"
                    late_object = Late.objects.filter(date__contains=datetime.date(date_value), emp_id=employee.employee_id.employee_id, isEndorsed='1')[0]
                    late_message = late_object.sms_text

                elif Late.objects.filter(date__contains=datetime.date(date_value), emp_id=employee.employee_id.employee_id, isEndorsed='2').exists():
                    if endorsement != '':
                        endorsement = "Habitual Late" + ' # ' + endorsement
                    else:
                        endorsement = " Habitual Late"

                    late_object = Late.objects.filter(date__contains=datetime.date(date_value), emp_id=employee.employee_id.employee_id, isEndorsed='2')[0]
                    late_message = late_object.sms_text

                else:
                    if endorsement != '':
                        endorsement = " Not Endorsed" + ' # ' + endorsement
                    else:
                        endorsement = "Not Endorsed"


        except ObjectDoesNotExist:
            in_time = 'N/A'

        try:
            out_in = get_out_in(employee.employee_id.cardId, date_value)
            emp_out_time = AttendanceHistory.objects.filter(emp_card_id=employee.employee_id.cardId,
                                                           in_out=out_in,
                                                           date=date_value).order_by('-id')[0:1].get()
            out_time = datetime.strptime(emp_out_time.time, "%H:%M:%S")
            out_time = out_time.strftime("%I:%M %p")

        except ObjectDoesNotExist:
            out_time = 'N/A'

        '''if in_time != 'N/A' and out_time != 'N/A':

            status = "<span class=\"label label-warning\">Present</span>"
            late_message = ""
            login_limit = office_time.office_start_time
        '''
        if in_time == 'N/A' and out_time == 'N/A':
            status = "<span class=\"label label-danger\">Absent</span>"
            endorsement=''
            login_limit = "N/A"
            day_status = 'absent'

        elif (in_time == 'N/A' and out_time != 'N/A'):
            status = "<span class=\"label label-warning\" style='background-color: #42209e;'>I/R</span>"
            day_status = 'ir'

        elif (in_time != 'N/A' and out_time == 'N/A'):
            ''' status = "<span class=\"label label-warning\" style='background-color: #42209e;'>I/R</span>"
            count_ir += 1
            '''
            pass

        if YearlyHoliday.objects.filter(date=date_value).exists():

            status = "Holiday"

            login_limit = "N/A"
            endorsement = ''
            late_message = ""

            working_day = False
            day_status = ''
            attendance_in_holiday = True

        elif WeeklyHoliday.objects.filter(effectiveFrom__lte=date_value, effectiveEnd__gte=date_value.date(), dayNum=date_value.isoweekday(), active_location=employee.location_id).exists():

            status = "Weekend"

            login_limit = "N/A"
            endorsement = ""
            late_message = ""

            working_day = False
            attendance_in_holiday = True



    elif YearlyHoliday.objects.filter(date=date_value).exists():

        status = "Holiday"
        in_time = ""
        out_time = ""
        login_limit = "N/A"
        endorsement = ''
        late_message = ""

        working_day = False
        day_status = ''

    elif WeeklyHoliday.objects.filter(effectiveFrom__lte=date_value, effectiveEnd__gte=date_value.date(), dayNum=date_value.isoweekday(), active_location=employee.location_id).exists():

        status = "Weekend"
        in_time = ""
        out_time = ""
        login_limit = "N/A"
        endorsement = ""
        late_message = ""

        working_day = False

    elif LeaveDetail.objects.filter(date=date_value, leave_id__employee_id=employee.employee_id.employee_id, leave_id__endorsement='1', isActive=True).exists():

        try:
            leave_obj = LeaveDetail.objects.get(date=date_value, leave_id__employee_id=employee.employee_id.employee_id, leave_id__endorsement='1', isActive=True)
            leave_label = leave_obj.leave_id.type.name
        except MultipleObjectsReturned:
            leave_label = 'Unrecongnized Leave'

        day_status = 'leave'

        status = "<span class=\"label label-warning\" style='background-color: #1370BF;'>" + leave_label +"</span>"
        in_time = ""
        out_time = ""
        login_limit = "N/A"
        endorsement = ""
        late_message = ""

        working_day = True


    elif LeaveDetail.objects.filter(date=date_value, leave_id__employee_id=employee.employee_id.employee_id, leave_id__endorsement='0', isActive=True).exists():

        day_status = 'absent'

        status = "<span class=\"label label-danger\">Absent</span>"
        endorsement = "Leave Application Pending"
        in_time = ""
        out_time = ""
        login_limit = "N/A"
        late_message = ""

        working_day = True

    else:
        status = "<span class=\"label label-danger\">Absent</span>"
        endorsement=''
        login_limit = "N/A"
        day_status = 'absent'



    return (working_day, status, day_status, in_time, out_time, login_limit, late_message, endorsement, late_status, attendance_in_holiday)



def get_entry_time(card_id, date):

    in_out = get_in_out(card_id,date)
    try:
        emp_in_time = AttendanceHistory.objects.filter(emp_card_id=card_id, in_out=in_out, date=date).order_by('id')[0:1].get()
        # in_time = datetime.strptime(emp_in_time.time, '%H:%M:%S')
        in_time = emp_in_time.time
        return in_time
    except ObjectDoesNotExist:
        return 'N/A'


def get_exit_time(card_id, date):
    try:
        emp_out_time = AttendanceHistory.objects.filter(emp_card_id=card_id,in_out='0',date=date).order_by('-id')[0:1].get()
        out_time = emp_out_time.time
        return out_time
    except ObjectDoesNotExist:
        return 'N/A'

def get_attendance_status(entry_time, date, location_id):

    try:
        office_time_obj = RegularOfficeTime.objects.get(start_effective_date__lte=date, end_effective_date__gte=date, location_id_id=location_id, isActive=True)
        office_time_with_grace = datetime(entry_time.year,entry_time.month,entry_time.day,office_time_obj.entry_time_with_grace.hour, office_time_obj.entry_time_with_grace.minute, office_time_obj.entry_time_with_grace.second)
        if entry_time <= office_time_with_grace:
            return 'Present'
        else:
            return 'Late'
    except ObjectDoesNotExist:
        return 'N/A'
    except MultipleObjectsReturned:
        return 'N/A'

def get_endorsement_status(emp_id, date):

    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=1)
    try:
        endorsement_obj = Late.objects.filter(emp_id_id=emp_id, isEndorsed='1', date__range=(start_date,end_date))[0:1].get()
        print('Date is')
        print(type(endorsement_obj.date.day))
        return True

    except ObjectDoesNotExist:
        return False

def get_in_out(card_id,date):

    reverse_location_list = ['Agrabad', 'LOBP', 'Kathgor', 'Tejgaon', 'HQ']
    in_out = '1'
    try:
        attendance_object = AttendanceHistory.objects.filter(emp_card_id=card_id, date=date)[0:1].get()

        if attendance_object.location in reverse_location_list:
            in_out = '0'
    except ObjectDoesNotExist:
        pass

    return in_out

def get_out_in(card_id,date):

    reverse_location_list = ['Agrabad', 'LOBP', 'Kathgor', 'Tejgaon', 'HQ']
    out_in = '0'
    try:
        attendance_object = AttendanceHistory.objects.filter(emp_card_id=card_id, date=date).last()

        if attendance_object.location in reverse_location_list:
            out_in = '1'
    except ObjectDoesNotExist:
        pass

    return out_in

