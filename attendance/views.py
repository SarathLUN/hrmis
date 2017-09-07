from django.shortcuts import render, get_object_or_404, redirect
from hr.models import Department,EmployeeDesignation,Employee, Location
from holiday.models import WeeklyHoliday,YearlyHoliday
from leave.models import LeaveDetail
from .models import AttendanceHistory, RegularOfficeTime, Attendance_exception,Late,sms, AttendanceReportSetting
from django.contrib.auth.decorators import login_required
from datetime import datetime,timedelta,date,time
from time import time
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.http import JsonResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .attendance_module_functions import get_entry_time,get_attendance_status,get_exit_time,get_in_out,get_out_in,get_attendance_information, get_attendance_information_extended
from account.models import EmployeeUser
from HRM.myScript import convert_to_date
from leave.models import LeaveHistory
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.core import serializers
from itertools import chain

from itertools import *
# Create your views here.

@login_required
def showAttendanceList(request):

    if request.is_ajax():
        data = {}
        department_id = request.POST.get('department')
        get_employee_list_for_dept = EmployeeDesignation.objects.filter(department_id_id=department_id, isActive=True).order_by('employee_id__employeeName')
        emp_list = []
        for emp in get_employee_list_for_dept:
            emp_list.append({'e_id' : emp.employee_id.employee_id, 'e_name' : emp.employee_id.employeeName})

        data['pDepartment'] = department_id
        data['emp_list'] = emp_list
        return JsonResponse(data)


    context = {}
    attendance_list = []
    start_date = convert_to_date(request.POST['startDate'])
    end_date = convert_to_date(request.POST['endDate'])
    dayCount = abs(end_date-start_date).days + 1
    employee_list = EmployeeDesignation.objects.filter(department_id_id = request.POST['department'], isActive=True).order_by('employee_id__employeeName')


    for employee_obj in employee_list:

        date_value = start_date

        for count in range(0,dayCount):


            if date_value.date() <= date.today():

                if employee_obj.employee_id.joiningDate > date_value.date():
                    attendance_list.append({'id' : employee_obj.employee_id.employee_id, 'designation' : employee_obj.des_id.designation ,'name' : employee_obj.employee_id.employeeName, 'card_id' : employee_obj.employee_id.cardId, 'date' : date_value.date(), 'in_time' : '', 'out_time' : '', 'login_limit' : '', 'status' : 'Has not Joined', 'late_message' : 'Has not Joined', 'endorsement' : 'Has not Joined', 'attendance_in_holiday' : 'Has not Joined'})

                else:
                    working_day, status, day_status, in_time, out_time, login_limit, late_message, endorsement, late_status, attendance_in_holiday = get_attendance_information_extended(date_value,employee_obj)

                    attendance_list.append({'id' : employee_obj.employee_id.employee_id, 'designation' : employee_obj.des_id.designation ,'name' : employee_obj.employee_id.employeeName, 'card_id' : employee_obj.employee_id.cardId, 'date' : date_value.date(), 'in_time' : in_time, 'out_time' : out_time, 'login_limit' : login_limit, 'status' : status, 'late_message' : late_message, 'endorsement' : endorsement, 'attendance_in_holiday' : attendance_in_holiday})

            '''
            if working_day:
                count_total_working_day += 1

            if late_status:
                count_late += 1

            if day_status == 'leave':
                count_on_leave += 1

            elif day_status == 'absent':
                count_absent += 1

            elif day_status == 'ir':
                count_ir += 1

                '''
            '''
            status = "Present"
            endorsement = ""
            if YearlyHoliday.objects.filter(date=date_value).exists():
                status = "Holiday"
                attendance_list.append({'id' : employee_obj.employee_id.employee_id, 'name' : employee_obj.employee_id.employeeName, 'card_id' : employee_obj.employee_id.cardId, 'date' : date_value.__format__('%b %d, %Y'), 'in_time' : "---", 'out_time' : "---", 'login_limit' : '', 'status' : status, 'designation' : employee_obj.des_id.designation})

            elif WeeklyHoliday.objects.filter(isActive=True, dayNum=date_value.isoweekday()):
                status = "Weekend"
                attendance_list.append({'id' : employee_obj.employee_id.employee_id, 'name' : employee_obj.employee_id.employeeName, 'card_id' : employee_obj.employee_id.cardId, 'date' : date_value.__format__('%b %d, %Y'), 'in_time' : "---", 'out_time' : "---", 'login_limit' : '', 'status' : status, 'designation' : employee_obj.des_id.designation})

            elif LeaveDetail.objects.filter(date=date_value, leave_id__employee_id=employee_obj.employee_id, leave_id__endorsement__in=('1','0'), isActive=True).exists():
                status = "On Leave"
                endorsement = ''
                if LeaveDetail.objects.filter(date=date_value, leave_id__employee_id=employee_obj.employee_id, leave_id__endorsement='0', isActive=True).exists():
                    status = "Absent"
                    endorsement = 'Application Pending'

                attendance_list.append({'id' : employee_obj.employee_id.employee_id, 'name' : employee_obj.employee_id.employeeName, 'card_id' : employee_obj.employee_id.cardId, 'date' : date_value.__format__('%b %d, %Y'), 'in_time' : "---", 'out_time' : "---", 'login_limit' : '', 'status' : status, 'designation' : employee_obj.des_id.designation, 'endorsement' : endorsement})

            else:
                try:
                    office_time = RegularOfficeTime.objects.get(start_effective_date__lte=date_value, end_effective_date__gte=date_value)

                    office_time_value = datetime(100,1,1,office_time.office_start_time.hour, office_time.office_start_time.minute, office_time.office_start_time.second)
                    print(type(office_time_value))
                    grace_time = office_time.grace_amount
                    office_time_with_grace_time = office_time_value + timedelta(minutes=grace_time)



                except ObjectDoesNotExist:
                    office_time = RegularOfficeTime.objects.get(start_effective_date__lte=date_value, isActive=True)


                try:
                    in_out = get_in_out(employee_obj.employee_id.cardId, date_value)
                    emp_in_time = AttendanceHistory.objects.filter(emp_card_id=employee_obj.employee_id.cardId,
                                                                   in_out=in_out,
                                                                   date=date_value).order_by('id')[0:1].get()
                    in_time = emp_in_time.time
                    in_time_value = datetime.strptime(in_time,"%H:%M:%S")
                    if in_time_value.time() > office_time_with_grace_time.time():
                        status = "Late"
                        if Late.objects.filter(date=date_value, emp_id=employee_obj.employee_id.employee_id, isEndorsed='1').exists():
                            endorsement = "Endorsed"
                        else:
                            endorsement = "Not Endorsed"

                except ObjectDoesNotExist:
                    in_time = 'N/A'


                try:
                    out_in = get_out_in(employee_obj.employee_id.cardId, date_value)
                    emp_out_time = AttendanceHistory.objects.filter(emp_card_id=employee_obj.employee_id.cardId,
                                                                   in_out=out_in,
                                                                   date=date_value).order_by('-id')[0:1].get()
                    out_time = emp_out_time.time

                except ObjectDoesNotExist:
                    out_time = 'N/A'

                if in_time != 'N/A' and out_time != 'N/A':

                    attendance_list.append({'id' : employee_obj.employee_id.employee_id, 'name' : employee_obj.employee_id.employeeName, 'card_id' : employee_obj.employee_id.cardId, 'date' : date_value.__format__('%b %d, %Y'), 'in_time' : in_time, 'out_time' : out_time, 'login_limit' : office_time.office_start_time, 'status' : status, 'endorsement' : endorsement, 'designation' : employee_obj.des_id.designation})

                elif in_time == 'N/A' and out_time == 'N/A' and date_value.date() < date.today():
                    status = "Absent"
                    attendance_list.append({'id' : employee_obj.employee_id.employee_id, 'name' : employee_obj.employee_id.employeeName, 'card_id' : employee_obj.employee_id.cardId, 'date' : date_value.__format__('%b %d, %Y'), 'in_time' : in_time, 'out_time' : out_time, 'login_limit' : office_time.office_start_time, 'status' : status, 'designation' : employee_obj.des_id.designation})

                elif (in_time == 'N/A' or out_time == 'N/A') and date_value.date() < date.today():
                    status = "I/R"
                    attendance_list.append({'id' : employee_obj.employee_id.employee_id, 'name' : employee_obj.employee_id.employeeName, 'card_id' : employee_obj.employee_id.cardId, 'date' : date_value.__format__('%b %d, %Y'), 'in_time' : in_time, 'out_time' : out_time, 'login_limit' : office_time.office_start_time, 'status' : status, 'endorsement' : endorsement, 'designation' : employee_obj.des_id.designation})

            '''

            date_value = date_value + timedelta(days=1)

    context['dept_attendance_list'] = attendance_list
    context['employee_dept'] = employee_list[0].department_id.departmentName
    context['start_date'] = start_date
    context['end_date'] = end_date

    legend = {'NOT APPLIED' : 'N/A', 'INTERVENTION REQUIRED' : 'I/R'}
    context['legend'] = legend

    employee_list = Employee.objects.all()
    context['employee_list'] = employee_list
    department_list = Department.objects.all().order_by('departmentName')
    context['department_list'] = department_list

    return render(request,'attendance/getAttendanceHistory.html', context)


@login_required
def getEmployeeAttendaceHistory(request):

    context = {}
    if request.is_ajax():
        data = {}
        department_id = request.POST.get('department')
        get_employee_list_for_dept = EmployeeDesignation.objects.filter(department_id_id=department_id, isActive=True).order_by('employee_id__employeeName')
        emp_list = []
        for emp in get_employee_list_for_dept:
            emp_list.append({'e_id' : emp.employee_id.employee_id, 'e_name' : emp.employee_id.employeeName})

        data['pDepartment'] = department_id
        data['emp_list'] = emp_list
        return JsonResponse(data)

    if request.method == "POST":

        count_total_working_day = 0
        count_present = 0
        count_on_leave = 0
        count_absent = 0
        count_late = 0
        count_ir = 0
        count_attendance_in_holiday = 0


        attendance_list = []
        start_date = convert_to_date(request.POST['startDate'])
        end_date = convert_to_date(request.POST['endDate'])
        dayCount = abs(end_date-start_date).days + 1
        employee_obj = get_object_or_404(Employee,pk=request.POST['employee'])

        date_value = start_date
        employee_detail = EmployeeDesignation.objects.filter(employee_id=employee_obj).order_by('effective_date_start').first()


        for count in range(0,dayCount):

            if employee_obj.joiningDate > date_value.date():
                attendance_list.append({'id' : employee_obj.employee_id, 'name' : employee_obj.employeeName, 'card_id' : employee_obj.cardId, 'date' : date_value.date(), 'in_time' : '', 'out_time' : '', 'login_limit' : '', 'status' : 'Has not Joined', 'late_message' : 'Has not Joined', 'endorsement' : 'Has not Joined', 'attendance_in_holiday' : 'Has not Joined'})

            elif employee_detail.effective_date_start > date_value.date():
                remarks ='No Designation Assigned'
                status = ''
                endorsement = ''
                in_time = '-'
                out_time = '-'
                if YearlyHoliday.objects.filter(date=date_value.date()).exists():
                    status = 'Yearly Holiday'
                    attendance_list.append({'id' : employee_obj.employee_id, 'name' : employee_obj.employeeName, 'card_id' : employee_obj.cardId, 'date' : date_value.date(), 'in_time' : in_time, 'out_time' : out_time, 'login_limit' : '', 'status' : status, 'late_message' : remarks, 'endorsement' : remarks, 'attendance_in_holiday' : remarks})

                elif WeeklyHoliday.objects.filter(effectiveFrom__lte=date_value.date(), effectiveEnd__gte=date_value.date(), dayNum=date_value.isoweekday(), active_location = employee_detail.location_id).exists():
                    status = 'Weekly Holiday'
                    attendance_list.append({'id' : employee_obj.employee_id, 'name' : employee_obj.employeeName, 'card_id' : employee_obj.cardId, 'date' : date_value.date(), 'in_time' : in_time, 'out_time' : out_time, 'login_limit' : '', 'status' : status, 'late_message' : remarks, 'endorsement' : remarks, 'attendance_in_holiday' : remarks})

                else:

                    in_time = get_entry_time(employee_obj.cardId, date_value.date())
                    out_time = get_exit_time(employee_obj.cardId, date_value.date())

                    count_total_working_day += 1

                    if in_time != 'N/A':
                        status = 'Present'
                        count_present += 1
                        in_time = datetime.strptime(in_time, '%H:%M:%S')
                        in_time = in_time.strftime("%I:%M %p")
                    if out_time != 'N/A':
                        out_time = datetime.strptime(out_time, '%H:%M:%S')
                        out_time = out_time.strftime("%I:%M %p")
                    if in_time == 'N/A' and out_time == 'N/A':
                        count_absent += 1
                        status = 'Absent'

                    attendance_list.append({'id' : employee_obj.employee_id, 'name' : employee_obj.employeeName, 'card_id' : employee_obj.cardId, 'date' : date_value.date(), 'in_time' : in_time, 'out_time' : out_time, 'login_limit' : '', 'status' : status, 'late_message' : remarks, 'endorsement' : remarks, 'attendance_in_holiday' : remarks})

            else:
                try:
                    employee_detail = EmployeeDesignation.objects.filter(employee_id=employee_obj, effective_date_start__lte=date_value, effective_date_end__gte=date_value).latest('emp_des_id')
                except:
                    employee_detail = EmployeeDesignation.objects.filter(employee_id=employee_obj, effective_date_start__lte=date_value, effective_date_end=None).latest('emp_des_id')

                if date_value.date() <= date.today():

                    working_day, status, day_status, in_time, out_time, login_limit, late_message, endorsement, late_status, attendance_in_holiday = get_attendance_information_extended(date_value,employee_detail)


                    attendance_list.append({'id' : employee_obj.employee_id, 'name' : employee_obj.employeeName, 'card_id' : employee_obj.cardId, 'date' : date_value.date(), 'in_time' : in_time, 'out_time' : out_time, 'login_limit' : login_limit, 'status' : status, 'late_message' : late_message, 'endorsement' : endorsement, 'attendance_in_holiday' : attendance_in_holiday})


                    if working_day:
                        count_total_working_day += 1

                    if late_status and (attendance_in_holiday==False):
                        count_late += 1

                    if attendance_in_holiday:
                        count_attendance_in_holiday += 1

                    if day_status == 'leave':
                        count_on_leave += 1

                    elif day_status == 'absent':
                        count_absent += 1

                    elif day_status == 'ir':
                        count_ir += 1

            date_value = date_value + timedelta(days=1)

        count_present = count_total_working_day - (count_on_leave + count_absent + count_ir)

        context['attendance_list'] = attendance_list
        context['employee_obj'] = employee_detail
        context['start_date'] = start_date
        context['end_date'] = end_date

        legend = {'NOT APPLIED' : 'N/A', 'INTERVENTION REQUIRED' : 'I/R'}
        count_present = count_total_working_day - (count_absent + count_on_leave)
        count_list = {'Total' : count_total_working_day,
                      'Present' : count_present,
                      'Absent' : count_absent,
                      'Late' : count_late,
                      'Leave' : count_on_leave,
                      'I_R' : count_ir,
                      'count_attendance_in_holiday' : count_attendance_in_holiday}
        print(count_list)
        context['legend'] = legend
        context['count_list'] = count_list

    employee_list = Employee.objects.all()
    context['employee_list'] = employee_list
    department_list = Department.objects.all().order_by('departmentName')
    context['department_list'] = department_list

    return render(request,'attendance/getAttendanceHistory.html', context)


@login_required
def dailyAttendaceReport(request):

    return render(request, 'attendance/daily_attendance_report.html')

@login_required
def addRegularOfficeTime(request, message_id):

    context = {}

    if request.method == "POST":

        entry_time = datetime.strptime(request.POST['entry_time'], "%I:%M %p")
        exit_time = datetime.strptime(request.POST['exit_time'], "%I:%M %p")
        grace_amount = int(request.POST['grace_amount'])
        entry_time_with_grace = entry_time + timedelta(minutes=grace_amount)

        if 'special_office_time' in request.POST:
            entry_category = '3'
        else:
            entry_category = '1'

        selected_location = request.POST.getlist('locations')

        for location in selected_location:
            try:
                current_office_time = RegularOfficeTime.objects.filter(isActive=True, location_id_id=location)
                for list in current_office_time:
                    list.isActive = False
                    list.end_effective_date = datetime.strptime(request.POST['start_date'], "%Y/%m/%d") - timedelta(days=1)
                    list.updateUser = request.user.id
                    list.updateDate = date.today()
                    list.save()
            except:
                pass


            new_office_time = RegularOfficeTime(office_start_time=entry_time,
                                                office_end_time=exit_time,
                                                grace_amount=grace_amount,
                                                entry_time_with_grace=entry_time_with_grace,
                                                start_effective_date=datetime.strptime(request.POST['start_date'], "%Y/%m/%d"),
                                                end_effective_date=datetime.max.date(),
                                                remarks='',
                                                entry_category=entry_category,
                                                location_id_id=location,
                                                isActive=True,
                                                insertUser=request.user.id,
                                                insertDate=date.today())
            new_office_time.save()

    try:
        office_time_list = RegularOfficeTime.objects.filter(isActive=True, end_effective_date__gte=date.today())
        context['office_time_list'] = office_time_list
    except ObjectDoesNotExist:
        context['office_time_message'] = 'No Office Schedule is Entered'


    location_list = Location.objects.filter(isActive=True).order_by('locationName')
    context['location_list'] = location_list

    return render(request, 'attendance/addRegularOfficeTime.html', context)


@login_required
def addExceptionOfficeTime(request):

    context = {}



    if request.method == "POST":
        t_date = convert_to_date(request.POST['date'])


        selected_location_list = request.POST.getlist('locations')

        for location_id in selected_location_list:

            office_time_obj = RegularOfficeTime.objects.get(isActive=True,location_id_id=location_id)

            if 'time_flexible' in request.POST:
                entry_time_with_grace = office_time_obj.office_end_time
                grace_amount = -99
            else:
                grace_amount = int(request.POST['grace_time'])
                office_time_value  = datetime(100,1,1,office_time_obj.office_start_time.hour, office_time_obj.office_start_time.minute, office_time_obj.office_start_time.second)
                entry_time_with_grace = office_time_value + timedelta(minutes=grace_amount)

            reg_obj, created = RegularOfficeTime.objects.get_or_create(start_effective_date=t_date,
                                                                       end_effective_date=t_date,
                                                                       entry_category='2',
                                                                       location_id_id = location_id,
                                                                       defaults={ 'office_start_time' : office_time_obj.office_start_time,
                                                                                  'office_end_time' : office_time_obj.office_end_time,
                                                                                  'grace_amount' : grace_amount,
                                                                                  'entry_time_with_grace' : entry_time_with_grace,
                                                                                  'remarks' : request.POST['reason'],
                                                                                  'description' : request.POST['description'],
                                                                                  'isActive' : False,
                                                                                  'insertUser' : request.user.id,
                                                                                  'insertDate' : date.today()
                                                                                  })
            if created:

                office_time_obj.isActive = False
                office_time_obj.end_effective_date = t_date - timedelta(days=1)
                office_time_obj.updateUser = request.user.id
                office_time_obj.updateDate = date.today()

                office_time_obj.save()

                new_office_time_exception = Attendance_exception(date=t_date,
                                                                 grace_time=grace_amount,
                                                                 cause=request.POST['reason'],
                                                                 description=request.POST['description'],
                                                                 location_id_id=location_id,
                                                                 isActive=True,
                                                                 insertUser=request.user.id,
                                                                 insertDate=date.today(),
                                                                 project='1'
                                                                 )
                new_office_time_exception.save()

                new_office_time = RegularOfficeTime(office_start_time=office_time_obj.office_start_time,
                                                    office_end_time=office_time_obj.office_end_time,
                                                    grace_amount=office_time_obj.grace_amount,
                                                    entry_time_with_grace=office_time_obj.entry_time_with_grace,
                                                    start_effective_date=t_date + timedelta(days=1),
                                                    end_effective_date=datetime.max.date(),
                                                    remarks='',
                                                    entry_category=office_time_obj.entry_category,
                                                    location_id_id=location_id,
                                                    isActive=True,
                                                    insertUser=request.user.id,
                                                    insertDate=date.today())
                new_office_time.save()

                context['form_message'] = "Successfully Inserted"

              #  context['form_message'] = "Exception for the date " + request.POST['date'] + " is already inserted"
            else:
                context['form_message'] = "Exception Entry for the date is already inserted!!"


    exception_list = Attendance_exception.objects.filter(date__year=date.today().year, isActive=True)
    context['exception_list'] = exception_list

    location_list = Location.objects.filter(isActive=True).order_by('locationName')
    context['location_list']= location_list


    return render(request, 'attendance/addExceptionOfficeTime.html', context)


@login_required
def lateAttendance(request):
    context = {}

    if request.is_ajax():


        data = {}

        if request.POST.get('ajax_option') == '2':

            emp_id = request.POST.get('emp_id')
            data['val'] = emp_id
            message_list = Late.objects.filter(emp_id_id=emp_id)
            obj = serializers.serialize('json', [message_list])
            print(obj)
            data['message_list'] = obj
            return JsonResponse(data)

        choice = request.POST.get('endorsement_id')
        sms_id = int(request.POST.get('msg_id'))
        try:
            late_obj = Late.objects.get(id=sms_id)

            late_obj.isEndorsed = choice
            late_obj.endorsed_by_id = request.user.employeeuser.employee_id

            late_obj.save()

            data['choice'] = choice

        except ObjectDoesNotExist:
            data['choice'] = 'none'


        return JsonResponse(data)


    try:
        employee_list = EmployeeDesignation.objects.filter(supervisor_id=request.user.employeeuser.employee.employee_id, isActive=True).order_by('employee_id__employeeName').values('employee_id_id')
        late_history = Late.objects.filter(emp_id_id__in=employee_list, isActive=True, isEndorsed='0').order_by('-date')
        previous_history = Late.objects.filter(emp_id_id__in=employee_list, isActive=True, isEndorsed__in=['1','2','3','4'], date__year='2016').order_by('emp_id__employeeName','-date')
        context['previous_history'] = previous_history
        print(previous_history)
        paginator = Paginator(late_history, 100)
        page = request.GET.get('page')

        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_pages)

        context['contacts'] = contacts
        context['late_history'] = late_history


    except:
        context['error_message'] = '!!! This page is for User type Employee !!!'

    '''
    try:
        employee_list = EmployeeDesignation.objects.filter(supervisor_id=request.user.employeeuser.employee.employee_id, isActive=True).order_by('employee_id__employeeName')
        late_history = []
        current_month_late_history = []
        checker = " "

        for list in employee_list:
            obj_list = Late.objects.filter(emp_id=list.employee_id, isActive=True).order_by('-date')
            #entry_time_list = ['0']
            for val in obj_list:
                entry_time = get_entry_time(val.emp_id.cardId,val.date)
                check_sms = val.sms_text.find(checker, 1, 20)
                if check_sms == -1:
                    val.sms_text = "UNREADABLE MESSAGE !!!"
                    #print(val.sms_text)

                if val.isEndorsed == '0':
                    late_history.append({'id' : val.id,
                                         'name' : val.emp_id.employeeName,
                                         'entry_time' : entry_time,
                                         'reason' : val.sms_text,
                                         'date' : val.date})
                    #entry_time_list.append(entry_time)
                else:
                    current_month_late_history.append({'id' : val.id,
                                                       'name' : val.emp_id.employeeName,
                                                       'entry_time' : entry_time,
                                                       'reason' : val.sms_text,
                                                       'date' : val.date,
                                                       'status' : val.get_isEndorsed_display()})


        #context['entry_time_list'] = entry_time_list
        context['late_history'] = late_history
        context['current_month_late_history'] = current_month_late_history
    except ObjectDoesNotExist:
        context['error_message'] = '!!! This page is for User type Employee !!!'

    '''


    return render(request, 'attendance/lateAttendance.html', context)




@login_required
def lateEndorsement(request, late_id, choice):

    late_obj = Late.objects.get(id=late_id)
    if choice == 'lateaccept':
        late_obj.isEndorsed = '1'
        late_obj.isActive = True
        '''
        edited on 7/20/2016 by tusfiqur alam
        '''
        #late_obj.endorsed_by = request.user.employeeuser.employee
        '''end edit'''
    elif choice == 'latereject':
        late_obj.isEndorsed = '2'
        late_obj.isActive = True

    elif choice =='otheraccept':
        late_obj.isEndorsed = '3'
        late_obj.isActive = True

    elif choice =='otherreject':
        late_obj.isEndorsed = '4'
        late_obj.isActive = True

    '''
    edited on 7/20/2016 by tusfiqur alam
    '''
    late_obj.endorsed_by = request.user.employeeuser.employee
    '''end edit'''
    late_obj.save()

    return HttpResponseRedirect(reverse('attendance:lateAttendance'))


@login_required
def readSms(request):


    context = {}

    unread_sms_list = sms.objects.filter(sms_table=None)

    context['unread_sms_list'] = unread_sms_list

    return render(request, 'attendance/lateSms.html', context)


@login_required
def deleteSms(request,sms_id):
    context = {}

    try:
        sms_obj = sms.objects.get(id=sms_id)
        sms_obj.delete()
        message = 'SMS successfully deleted!!'

    except:
        message = 'SMS not found!!'

    context['form_message'] = message
    unread_sms_list = sms.objects.filter(sms_table=None)

    context['unread_sms_list'] = unread_sms_list

    return render(request, 'attendance/lateSms.html', context)


@login_required
def generate_sms_to_late(request):

    unread_sms_list = sms.objects.filter(sms_table=None)

    for list in unread_sms_list:
        if list.date_time[0] == '':
            date_value = list.date_time[1:]
        if list.date_time[4] == '/':
            date_value = list.date_time[0:4] + '-' + list.date_time[5:7] + '-' + list.date_time[8:]

            print(date_value)

        else:
            date_value = list.date_time
        try:
            date_value1 = datetime.strptime(date_value, '%Y-%m-%d %H:%M:%S')
            date_value = date_value1.strftime('%Y-%m-%d %H:%M:%SZ')
            #date_value = date_value + timedelta(hours=6)
            emp = Employee.objects.get(mobile=list.mobile_no)
            new_late_obj = Late(date=date_value,
                                isEndorsed='0',
                                sms_text=list.sms_text,
                                isActive=True,
                                isDelete=False,
                                insertUser=request.user.id,
                                insertDate=date.today(),
                                project='1',
                                emp_id=emp,
                                sms_table_id=list)
            new_late_obj.save()

        except ObjectDoesNotExist:
            pass

    return HttpResponseRedirect(reverse('attendance:readsms'))

@login_required
def get_own_attendance(request):
    context = {}
    '''
    if request.is_ajax():
        data = {}
        department_id = request.POST.get('department')
        get_employee_list_for_dept = EmployeeDesignation.objects.filter(department_id_id=department_id)
        emp_list = []
        for emp in get_employee_list_for_dept:
            emp_list.append({'e_id' : emp.employee_id.employee_id, 'e_name' : emp.employee_id.employeeName})

        data['pDepartment'] = department_id
        data['emp_list'] = emp_list
        return JsonResponse(data)

    '''

    employee_user = EmployeeUser.objects.get(user_id=request.user.id)
    employee_obj = get_object_or_404(Employee,pk=employee_user.employee.employee_id)

    subordinate_list = EmployeeDesignation.objects.filter(isActive=True, supervisor=employee_obj).values_list('employee_id__employee_id', 'employee_id__employeeName')
    context['subordinate_list'] = subordinate_list

    child_list = AttendanceReportSetting.objects.filter(parent_employee=employee_obj, isActive=True).values_list('child_employee__employee_id', 'child_employee__employeeName')
    context['child_list'] = child_list

    # result_list = list(chain(subordinate_list, child_list))
    result_list = list(set(subordinate_list)|set(child_list))
    context['result_list'] = result_list
    #print(result_list)

    if request.method == "POST":

        count_total_working_day = 0
        count_present = 0
        count_on_leave = 0
        count_absent = 0
        count_late = 0
        count_ir = 0
        count_attendance_in_holiday = 0

        attendance_list = []
        start_date = convert_to_date(request.POST['startDate'])
        end_date = convert_to_date(request.POST['endDate'])

        #date_range = request.POST['hidden_date_range']

        #date_range_value = date_range.split('-')
        #print(date_range_value)
        #start_date_range = date_range_value[0]
        #start_date = datetime.strptime(date_range_value[0],"%B %d, %Y ")
        #end_date = datetime.strptime(date_range_value[1]," %B %d, %Y")
        #context['date_range'] = date_range_value
        #print(date_range)


        dayCount = abs(end_date-start_date).days + 1
        try:
            if 'own_report' not in request.POST and 'child_emp_id' not in request.POST:
                employee_user = EmployeeUser.objects.get(user_id=request.user.id)
                employee_obj = get_object_or_404(Employee,pk=employee_user.employee.employee_id)

            elif 'own_report' in request.POST:
                employee_user = EmployeeUser.objects.get(user_id=request.user.id)
                employee_obj = get_object_or_404(Employee,pk=employee_user.employee.employee_id)
            else:
                employee_obj = get_object_or_404(Employee,pk=request.POST['child_emp_id'])


            date_value = start_date


            employee_detail = EmployeeDesignation.objects.filter(employee_id=employee_obj).order_by('effective_date_start').first()


            for count in range(0,dayCount):

                if employee_obj.joiningDate > date_value.date():
                    attendance_list.append({'id' : employee_obj.employee_id, 'name' : employee_obj.employeeName, 'card_id' : employee_obj.cardId, 'date' : date_value.date(), 'in_time' : '', 'out_time' : '', 'login_limit' : '', 'status' : 'Has not Joined', 'late_message' : 'Has not Joined', 'endorsement' : 'Has not Joined', 'attendance_in_holiday' : 'Has not Joined'})

                elif employee_detail.effective_date_start > date_value.date():

                    in_time = get_entry_time(employee_obj.cardId, date_value.date())
                    out_time = get_exit_time(employee_obj.cardId, date_value.date())
                    attendance_list.append({'id' : employee_obj.employee_id, 'name' : employee_obj.employeeName, 'card_id' : employee_obj.cardId, 'date' : date_value.date(), 'in_time' : in_time, 'out_time' : out_time, 'login_limit' : '', 'status' : 'No Designation Assigned', 'late_message' : 'No Designation Assigned', 'endorsement' : 'No Designation Assigned', 'attendance_in_holiday' : 'No Designation Assigned'})

                else:
                    try:
                        employee_detail = EmployeeDesignation.objects.filter(employee_id=employee_obj, effective_date_start__lte=date_value, effective_date_end__gte=date_value).latest('emp_des_id')
                    except:
                        employee_detail = EmployeeDesignation.objects.filter(employee_id=employee_obj, effective_date_start__lte=date_value, effective_date_end=None).latest('emp_des_id')

                    if date_value.date() <= date.today():

                        working_day, status, day_status, in_time, out_time, login_limit, late_message, endorsement, late_status, attendance_in_holiday = get_attendance_information_extended(date_value,employee_detail)


                        attendance_list.append({'id' : employee_obj.employee_id, 'name' : employee_obj.employeeName, 'card_id' : employee_obj.cardId, 'date' : date_value.date(), 'in_time' : in_time, 'out_time' : out_time, 'login_limit' : login_limit, 'status' : status, 'late_message' : late_message, 'endorsement' : endorsement, 'attendance_in_holiday' : attendance_in_holiday})


                        if working_day:
                            count_total_working_day += 1

                        if late_status and (attendance_in_holiday==False):
                            count_late += 1

                        if attendance_in_holiday:
                            count_attendance_in_holiday += 1

                        if day_status == 'leave':
                            count_on_leave += 1

                        elif day_status == 'absent':
                            count_absent += 1

                        elif day_status == 'ir':
                            count_ir += 1

                date_value = date_value + timedelta(days=1)


            count_present = count_total_working_day - (count_on_leave + count_absent + count_ir)

            context['attendance_list'] = attendance_list

            context['employee_obj'] = employee_detail

            context['start_date'] = start_date
            context['end_date'] = end_date

            legend = {'NOT APPLIED' : 'N/A', 'INTERVENTION REQUIRED' : 'I/R'}
            count_present = count_total_working_day - (count_absent + count_on_leave)
            count_list = {'Total' : count_total_working_day,
                          'Present' : count_present,
                          'Absent' : count_absent,
                          'Late' : count_late,
                          'Leave' : count_on_leave,
                          'I_R' : count_ir,
                          'count_attendance_in_holiday' : count_attendance_in_holiday}
            #print(count_list)

            context['legend'] = legend
            context['count_list'] = count_list


        except ObjectDoesNotExist:
            context['error_message'] = 'This Page is for Employee User'


    return render(request, 'attendance/user_attendance_history.html', context)

@login_required
def absent_report(request):

    context = {}

    if request.method == "POST":

        count_total_working_day = 0
        count_absent = 0
        count_unapplied = 0
        count_leave = 0


        attendance_list = []
        start_date = convert_to_date(request.POST['startDate'])
        end_date = convert_to_date(request.POST['endDate'])
        dayCount = abs(end_date-start_date).days + 1

        employee_user = EmployeeUser.objects.get(user_id=request.user.id)
        employee_obj = get_object_or_404(Employee,pk=employee_user.employee.employee_id)

        employee_detail = EmployeeDesignation.objects.filter(employee_id=employee_obj).latest('emp_des_id')

        date_value = start_date


        for count in range(0,dayCount):

            working_day, status, day_status, in_time, out_time, login_limit, late_message, endorsement, late_status, attendance_in_holiday = get_attendance_information_extended(date_value,employee_detail)



            if day_status == 'absent':
                attendance_list.append({'id' : employee_obj.employee_id, 'name' : employee_obj.employeeName, 'card_id' : employee_obj.cardId, 'date' : date_value.date(), 'in_time' : in_time, 'out_time' : out_time, 'login_limit' : login_limit, 'status' : status, 'late_message' : late_message, 'endorsement' : endorsement, 'attendance_in_holiday' : attendance_in_holiday})
                count_absent += 1
                if endorsement=='':
                    count_unapplied += 1

                count_total_working_day += 1

            elif day_status == 'leave':
                attendance_list.append({'id' : employee_obj.employee_id, 'name' : employee_obj.employeeName, 'card_id' : employee_obj.cardId, 'date' : date_value.date(), 'in_time' : in_time, 'out_time' : out_time, 'login_limit' : login_limit, 'status' : status, 'late_message' : late_message, 'endorsement' : endorsement, 'attendance_in_holiday' : attendance_in_holiday})
                count_leave += 1

                count_total_working_day += 1

            date_value = date_value + timedelta(days=1)

        count_pending = count_total_working_day - (count_unapplied + count_leave)

        context['attendance_list'] = attendance_list
        context['employee_obj'] = employee_detail
        context['start_date'] = start_date
        context['end_date'] = end_date

        legend = {'NOT APPLIED' : 'N/A', 'INTERVENTION REQUIRED' : 'I/R'}

        count_list = {'Total' : count_total_working_day,
                      'Absent' : count_absent,
                      'unapplied' : count_unapplied,
                      'leave' : count_leave,
                      'pending' : count_pending,
                      }
        print(count_list)
        context['legend'] = legend
        context['count_list'] = count_list

    return render(request, 'attendance/absent_report.html', context)


@login_required
def employee_absent_report(request):
    context = {}

    if request.is_ajax():
        data = {}
        department_id = request.POST.get('department')
        get_employee_list_for_dept = EmployeeDesignation.objects.filter(department_id_id=department_id, isActive=True).order_by('employee_id__employeeName')
        emp_list = []
        for emp in get_employee_list_for_dept:
            emp_list.append({'e_id' : emp.employee_id.employee_id, 'e_name' : emp.employee_id.employeeName})

        data['pDepartment'] = department_id
        data['emp_list'] = emp_list
        return JsonResponse(data)

    if request.method == "POST":

        count_total_working_day = 0
        count_absent = 0
        count_unapplied = 0
        count_leave = 0


        attendance_list = []
        start_date = convert_to_date(request.POST['startDate'])
        end_date = convert_to_date(request.POST['endDate'])
        dayCount = abs(end_date-start_date).days + 1


        if 'all_employee' in request.POST:
            department = request.POST['department']
            employee_list = EmployeeDesignation.objects.filter(department_id_id=department, isActive=True)
            #print(employee_list)
            for employee_detail in employee_list:
                date_value = start_date
                for count in range(0,dayCount):

                    working_day, status, day_status, in_time, out_time, login_limit, late_message, endorsement, late_status, attendance_in_holiday = get_attendance_information_extended(date_value,employee_detail)



                    if day_status == 'absent':
                        attendance_list.append({'id' : employee_detail.employee_id.employee_id, 'name' : employee_detail.employee_id.employeeName, 'card_id' : employee_detail.employee_id.cardId, 'date' : date_value.date(), 'in_time' : in_time, 'out_time' : out_time, 'login_limit' : login_limit, 'status' : status, 'late_message' : late_message, 'endorsement' : endorsement})
                        count_absent += 1
                        if endorsement=='':
                            count_unapplied += 1

                        count_total_working_day += 1

                    elif day_status == 'leave':
                        attendance_list.append({'id' : employee_detail.employee_id.employee_id, 'name' : employee_detail.employee_id.employeeName, 'card_id' : employee_detail.employee_id.cardId, 'date' : date_value.date(), 'in_time' : in_time, 'out_time' : out_time, 'login_limit' : login_limit, 'status' : status, 'late_message' : late_message, 'endorsement' : endorsement})
                        count_leave += 1

                        count_total_working_day += 1

                    date_value = date_value + timedelta(days=1)

                count_pending = count_total_working_day - (count_unapplied + count_leave)

                context['attendance_list'] = attendance_list
                context['employee_obj'] = employee_detail
                context['start_date'] = start_date
                context['end_date'] = end_date

                legend = {'NOT APPLIED' : 'N/A', 'INTERVENTION REQUIRED' : 'I/R'}

                count_list = {'Total' : count_total_working_day,
                              'Absent' : count_absent,
                              'unapplied' : count_unapplied,
                              'leave' : count_leave,
                              'pending' : count_pending,
                              }
                #print(count_list)
                context['all_list'] = True
                context['legend'] = legend
                context['count_list'] = count_list


        else:
            date_value = start_date
            employee_obj = get_object_or_404(Employee,pk=request.POST['employee'])
            employee_detail = EmployeeDesignation.objects.filter(employee_id=employee_obj).latest('emp_des_id')

            for count in range(0,dayCount):

                working_day, status, day_status, in_time, out_time, login_limit, late_message, endorsement, late_status, attendance_in_holiday = get_attendance_information_extended(date_value,employee_detail)



                if day_status == 'absent':
                    attendance_list.append({'id' : employee_obj.employee_id, 'name' : employee_obj.employeeName, 'card_id' : employee_obj.cardId, 'date' : date_value.date(), 'in_time' : in_time, 'out_time' : out_time, 'login_limit' : login_limit, 'status' : status, 'late_message' : late_message, 'endorsement' : endorsement})
                    count_absent += 1
                    if endorsement=='':
                        count_unapplied += 1

                    count_total_working_day += 1

                elif day_status == 'leave':
                    attendance_list.append({'id' : employee_obj.employee_id, 'name' : employee_obj.employeeName, 'card_id' : employee_obj.cardId, 'date' : date_value.date(), 'in_time' : in_time, 'out_time' : out_time, 'login_limit' : login_limit, 'status' : status, 'late_message' : late_message, 'endorsement' : endorsement})
                    count_leave += 1

                    count_total_working_day += 1

                date_value = date_value + timedelta(days=1)

            count_pending = count_total_working_day - (count_unapplied + count_leave)

            context['attendance_list'] = attendance_list
            context['employee_obj'] = employee_detail
            context['start_date'] = start_date
            context['end_date'] = end_date

            legend = {'NOT APPLIED' : 'N/A', 'INTERVENTION REQUIRED' : 'I/R'}

            count_list = {'Total' : count_total_working_day,
                          'Absent' : count_absent,
                          'unapplied' : count_unapplied,
                          'leave' : count_leave,
                          'pending' : count_pending,
                          }
            #print(count_list)
            context['all_list'] = False
            context['legend'] = legend
            context['count_list'] = count_list


    department_list = Department.objects.all().order_by('departmentName')
    context['department_list'] = department_list


    return render(request, 'attendance/employee_absent_report.html', context)


@login_required
def movement_report(request):

    context = {}

    department_list = Department.objects.all().order_by('departmentName')

    if request.is_ajax():
        data = {}
        department_id = request.POST.get('department')
        get_employee_list_for_dept = EmployeeDesignation.objects.filter(department_id_id=department_id, isActive=True).order_by('employee_id__employeeName')
        emp_list = []
        for emp in get_employee_list_for_dept:
            emp_list.append({'e_id' : emp.employee_id.employee_id, 'e_name' : emp.employee_id.employeeName})

        data['pDepartment'] = department_id
        data['emp_list'] = emp_list
        return JsonResponse(data)

    if request.method == 'POST':

        start_date = convert_to_date(request.POST['startDate'])
        end_date = convert_to_date(request.POST['endDate'])
        dayCount = abs(end_date-start_date).days + 1
        employee_obj = get_object_or_404(Employee,pk=request.POST['employee'])
        date_value = start_date
        movement_list = []
        for count in range(0,dayCount):

            attendance_history_list = AttendanceHistory.objects.filter(emp_card_id=employee_obj.cardId,date=date_value)

            entry_status = 1
            last_in_time = ''
            first_entry = True

            if len(attendance_history_list) == 1:

                date_entry = "<a>" + date_value.strftime("%b %d, %Y") + "</a>"

                last_in_time = datetime.strptime(attendance_history_list[0].time,"%H:%M:%S")
                last_in_time = last_in_time.strftime("%I:%M %p")

                movement_list.append({'date' : date_entry, 'in_time' : last_in_time, 'out_time' : ''})

            else:
                for list in attendance_history_list:


                    if list.in_out == get_in_out(employee_obj.cardId, date_value):

                        if last_in_time != '':

                            if first_entry:
                                date_entry = "<a>" + date_value.strftime("%b %d, %Y") + "</a>"
                                first_entry = False
                            else:
                                date_entry = ''

                            movement_list.append({'date' : date_entry, 'in_time' : last_in_time, 'out_time' : ''})


                        last_in_time = datetime.strptime(list.time,"%H:%M:%S")
                        last_in_time = last_in_time.strftime("%I:%M %p")


                    elif list.in_out == get_out_in(employee_obj.cardId, date_value):

                        last_out_time = datetime.strptime(list.time,"%H:%M:%S")
                        last_out_time = last_out_time.strftime("%I:%M %p")

                        if first_entry:
                            date_entry = "<a>" + date_value.strftime("%b %d, %Y") + "</a>"
                            first_entry = False
                        else:
                            date_entry = ''

                        movement_list.append({'date' : date_entry, 'in_time' : last_in_time, 'out_time' :last_out_time})
                        last_in_time = ''

            date_value = date_value + timedelta(days=1)

        employee_detail = EmployeeDesignation.objects.filter(employee_id=employee_obj).latest('emp_des_id')

        context['movement_list'] = movement_list
        context['employee_obj'] = employee_detail
        context['start_date'] = start_date
        context['end_date'] = end_date

    context['department_list'] = department_list
    return render(request, 'attendance/movement_report.html', context)


@login_required
def view_user_sms(request):

    context = {}
    try:
        employee_user = EmployeeUser.objects.get(user_id=request.user.id, isActive=True)
        employee_obj = get_object_or_404(Employee,pk=employee_user.employee.employee_id)


        sms_list = Late.objects.filter(isActive=True, emp_id=employee_obj, date__year=date.today().year).order_by('-date')

        for list in sms_list:
            check_sms = list.sms_text.find(" ",1,20)
            if check_sms == -1:
                list.sms_text = "UNREADABLE MESSAGE !!!"

            list.date = list.date - timedelta(hours=6)
        context['sms_list'] = sms_list

    except:
        pass


    return render(request, 'attendance/view_sms_status.html', context)

@login_required
def attedance_report_setting(request):

    '''
    if request.is_ajax():
        data = {}
        ajax_parent = request.POST.get('parent_id')
        ajax_child_list = []
        obj_list = AttendanceReportSetting.objects.filter(parent_employee_id=ajax_parent, isActive=True)
        for list in obj_list:
            ajax_child_list.append(list.child_employee_id)

        data['ajax_child_list'] = ajax_child_list
        print(ajax_child_list)

        return JsonResponse(data)
    '''

    context = {}


    active_employee_list = EmployeeDesignation.objects.values('employee_id__employee_id', 'employee_id__employeeName', 'department_id__departmentName', 'des_id__designation').distinct()
    print(active_employee_list)
    if request.method == "POST":
        parent_id = request.POST['parent']
        old_list = []
        child_list = AttendanceReportSetting.objects.filter(parent_employee_id=parent_id, isActive=True)

        for list in child_list:
            old_list.append(list.child_employee.employee_id)

        context['parent_id'] = parent_id
        context['old_list'] = old_list
        '''child_id_list = request.POST.getlist('child_list')

        for list in child_id_list:
            relation_obj, created = AttendanceReportSetting.objects.get_or_create(parent_employee=get_object_or_404(Employee, pk=parent_id),
                                                                                  child_employee=get_object_or_404(Employee, pk=list),
                                                                                  isActive=True,
                                                                                  defaults= {
                                                                                      'insertUser' : request.user.id,
                                                                                      'insertDate' : date.today(),
                                                                                      'project' : '1',
                                                                                  })
        '''

    context['employee_list'] = active_employee_list.order_by('employee_id__employeeName')
    context['child_employee_list'] = active_employee_list.order_by('department_id__departmentName', 'employee_id__employeeName')
    return render(request, 'attendance/attendance_report_setting.html', context)

def parent_child_relation(request, parent_id):

    new_child_id_list = request.POST.getlist('child_list')

    old_child = AttendanceReportSetting.objects.filter(parent_employee=get_object_or_404(Employee, pk=parent_id), isActive=True).delete()

    for list in new_child_id_list:
        new_obj = AttendanceReportSetting(parent_employee_id=parent_id,
                                          child_employee_id=list,
                                          isActive=True,
                                          insertUser=request.user.id,
                                          insertDate=date.today(),
                                          project='1')

        new_obj.save()

    return HttpResponseRedirect(reverse('attendance:report_setting'))

def endorsement_report(request):

    context = {}

    if request.method == "POST":
        #start_date = convert_to_date(request.POST['startDate'])
        #end_date = convert_to_date(request.POST['endDate'])
        employee_obj = get_object_or_404(EmployeeDesignation,pk=request.POST['employee'])

        pending_leave = LeaveHistory.objects.filter(endorsement='0', endorsed_by_id=employee_obj.employee_id_id, isActive=True) | LeaveHistory.objects.filter(endorsement='3', confirmed_by=employee_obj.employee_id_id, isActive=True)
        #print(pending_leave)
        context['pending_leave'] = pending_leave.count()
        context['employee_obj'] = employee_obj

        # subordinate_list = EmployeeDesignation.objects.filter(isActive=True, supervisor=employee_obj.employee_id)
        # print(subordinate_list)

        #late_list = Late.objects.filter(isActive=True, emp_id_id__in=subordinate_list.values('employee_id_id'), isEndorsed='0', date__gte=subordinate_list.values('effective_date_start'), date__lte=subordinate_list.values('effective_date_end')).count()
        #context['late_list'] = late_list


    active_employee_list = EmployeeDesignation.objects.filter(isActive=True).order_by('employee_id__employeeName')

    context['active_employee_list'] = active_employee_list
    return render(request, 'attendance/endorsement_report.html', context)