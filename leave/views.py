from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect,JsonResponse, HttpResponse
from django.core.urlresolvers import reverse
from .models import LeaveCategory, LeaveAllotment,LeaveHistory, LeaveDetail
from django.contrib.auth.decorators import login_required
from hr.models import EmployeeDesignation, Employee
from attendance.models import Late
from holiday.models import WeekDays, WeeklyHoliday, YearlyHoliday
from datetime import date, datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from HRM.myScript import convert_to_date
from reportlab.pdfgen import canvas
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
# Create your views here.

@login_required
def addLeaveCategoryPage(request, message):

    category_list = LeaveCategory.objects.filter(isActive=True)
    context = {}
    context['category_list'] = category_list
    if message == 'add':
        context['form_message'] = ''
    elif message == 'True':
        context['form_message'] = 'New Category has been added successfully'
    elif message == 'False':
        context['form_message'] = 'Category with same name already Exists!! '
    elif message == 'edited':
        context['form_message'] = 'Category Successfully Edited'
    elif message == 'inactivated':
        context['form_message'] = 'Category inactivated'
    else:
        context['form_message'] = 'some Error Occurred'

    active_employee_list = EmployeeDesignation.objects.filter(isActive=True).order_by("employee_id__employeeName")
    context['active_employee_list'] = active_employee_list

    return render(request, 'leave/leaveCategoryAdd.html', context)


@login_required
def addLeaveCategoryPerfomed(request):
    effective_start_date = convert_to_date(request.POST['start_date'])
    leave_type = request.POST['leave_type_text']
    if request.POST['confirmed_by'] == '0':
        confirmed_by_value = None
        entitled = request.POST['entitled_radio']
        validity = request.POST['validity_radio']
        minimum_days = request.POST['minimum_days']

        obj, created = LeaveCategory.objects.get_or_create(name = request.POST['name'],
                                                  defaults={
                                                      'amount' : request.POST['amount'],
                                                      'effective_day_from' : effective_start_date,
                                                      'description' : request.POST['description'],
                                                      'isActive' : True,
                                                      'gender' : request.POST['leave_category_gender'],
                                                      'insertUser' : request.user.id,
                                                      'insertDate' : date.today(),
                                                      'leave_type' : leave_type,
                                                      'entitled' : entitled

                                                  })

    else:
        confirmed_by_value = request.POST['confirmed_by']

        obj, created = LeaveCategory.objects.get_or_create(name = request.POST['name'],
                                                  defaults={
                                                      'amount' : request.POST['amount'],
                                                      'effective_day_from' : effective_start_date,
                                                      'description' : request.POST['description'],
                                                      'confirmed_by_id' : confirmed_by_value,
                                                      'isActive' : True,
                                                      'gender' : request.POST['leave_category_gender'],
                                                      'insertUser' : request.user.id,
                                                      'insertDate' : date.today(),
                                                      'leave_type' : leave_type

                                                  })

    return redirect('leave:addLeaveCategoryPage', message=created)


@login_required
def editLeaveCategoryPage(request, category_id):

    context = {}
    if request.method == "POST":
        form_message = ''

        if request.POST["optionsRadios"] == 'edit':
            if request.POST["approved_by_select"] == '0':
                obj = get_object_or_404(LeaveCategory, pk=category_id)
                obj.name = request.POST['name']
                obj.description = request.POST['description']
                obj.amount = request.POST['amount']
                obj.gender = request.POST['leave_category_gender']
                obj.confirmed_by_id = None
                obj.updateUser = request.user.id
                obj.updateDate = date.today()

                obj.save()
            else:

                obj = get_object_or_404(LeaveCategory, pk=category_id)
                obj.name = request.POST['name']
                obj.description = request.POST['description']
                obj.amount = request.POST['amount']
                obj.gender = request.POST['leave_category_gender']
                obj.confirmed_by_id = request.POST['approved_by_select']
                obj.updateUser = request.user.id
                obj.updateDate = date.today()

                obj.save()

            form_message = 'edited'

        elif request.POST['optionsRadios'] == 'inactivate':
            effective_end_date = convert_to_date(request.POST['end_date'])
            obj = get_object_or_404(LeaveCategory, pk=category_id)
            obj.effective_day_to = effective_end_date
            obj.isActive = False
            obj.updateUser = request.user.id
            obj.updateDate = date.today()
            obj.save()
            form_message = 'inactivated'

        return redirect('leave:addLeaveCategoryPage', message=form_message)

    obj = get_object_or_404(LeaveCategory, pk=category_id)
    context['category'] = obj

    active_employee_list = EmployeeDesignation.objects.filter(isActive=True).order_by("employee_id__employeeName")
    context['active_employee_list'] = active_employee_list

    return render(request, 'leave/leaveCategoryEdit.html',context)


@login_required
def applyLeave(request,message):

    context = {}
    error_message = ''

    if request.is_ajax():
        data = {}
        ajax_type = request.POST.get('ajax_type')


        if ajax_type=='1':
            leave_type = request.POST.get('leave_type')
            supervisor = ''
            try:
                leave_obj = LeaveCategory.objects.get(id=leave_type)

                if leave_obj.confirmed_by != None:
                    ceo_obj = EmployeeDesignation.objects.filter(employee_id=leave_obj.confirmed_by, isActive=True).order_by('-effective_date_start')[0]
                    ajax_message = "This application will also be sent to " + ceo_obj.employee_id.get_gender_display() + " " + ceo_obj.employee_id.employeeName + " for confirmation"
                    ajax_description = leave_obj.description
                    supervisor = ceo_obj.employee_id.employee_id

                else:
                    #obj = EmployeeDesignation.objects.get(employee_id = request.user.employeeuser.employee, isActive=True)
                    ajax_message = ''
                    supervisor = '0'
                    ajax_description = ''


            except ObjectDoesNotExist:
                pass

            data['supervisor'] = supervisor
            data['ajax_message'] = ajax_message
            data['ajax_description'] = ajax_description

        else:
            startDate = datetime.strptime(request.POST.get('start_date'), "%Y/%m/%d")
            checkDate = startDate
            endDate = startDate - timedelta(days=1)
            total_amount = int(request.POST.get('total_amount'))

            try:
                emp_details = EmployeeDesignation.objects.get(employee_id = request.user.employeeuser.employee, isActive=True)

            except:
                emp_details = 0

            while total_amount:
                if WeeklyHoliday.objects.filter(effectiveFrom__lte=checkDate, effectiveEnd__gte=checkDate, dayNum=checkDate.isoweekday(), active_location=emp_details.location_id).exists() or YearlyHoliday.objects.filter(date=checkDate).exists():
                    endDate = endDate + timedelta(days=1)
                else:
                    endDate = endDate + timedelta(days=1)
                    total_amount -= 1

                checkDate = checkDate + timedelta(days=1)

            '''
            weekend_list = WeeklyHoliday.objects.filter(isActive=True)
            holiday_list = YearlyHoliday.objects.filter(date__range=(startDate,endDate))

            for d in range(0,dayCount):
                for weekend in weekend_list:
                    if checkDate.isoweekday() == weekend.dayNum:
                        totalDays = totalDays - 1
                      #  print(checkDate.date())
                       # print(totalDays)
                        break


                for holiday in holiday_list:
                    if checkDate.date() == holiday.date:
                        totalDays = totalDays - 1
                      #  print(checkDate.date())
                      #  print(totalDays)
                        break

                checkDate = checkDate + timedelta(days=1)

                '''

            data['end_date'] = endDate.strftime("%Y/%m/%d")

        return JsonResponse(data)


    try:
        obj = EmployeeDesignation.objects.get(employee_id = request.user.employeeuser.employee, isActive=True)
        context['employee_info'] = obj

        policy = True

        leaveCategory_obj_list = LeaveCategory.objects.filter(isActive=True, gender__in=[request.user.employeeuser.employee.gender,'0'])
        leave_balance_list = []

        for category in leaveCategory_obj_list:
            allocated_balance = category.amount

            if policy:
                try:
                    joining_date = obj.employee_id.joiningDate.year
                    if joining_date == date.today().year :
                        allocated_balance = round((category.amount / 365) * (365 - obj.employee_id.joiningDate.timetuple().tm_yday))

                except:
                    error_message = str(obj.supervisor_id) + "Incomplete Employee Info. \n No Joining Date!!!"
                    context['joining_date_null_error'] = error_message
                    allocated_balance = 'N/A'

            try:
                if category.leave_type == 0:
                    leave_balance = LeaveAllotment.objects.filter(leave_id__type__id = category.id, isActive=True, employee_id=obj.employee_id, year=date.today().year).latest('id')
                else:
                    leave_balance = LeaveAllotment.objects.filter(leave_id__type__id = category.id, isActive=True, employee_id=obj.employee_id, year=date.today().year).latest('id')

                leave_balance_list.append({'id' : category.id, 'name' : category.name, 'balance' : leave_balance.balance})

            except ObjectDoesNotExist:
                leave_balance_list.append({'id' : category.id, 'name' : category.name, 'balance' : allocated_balance})

        context['balance_list'] = leave_balance_list
        context['leave_category'] = leaveCategory_obj_list

        # retriving leave application history
        leave_application_histroy = LeaveHistory.objects.filter(employee_id=request.user.employeeuser.employee, date_from__year=date.today().year, isActive=True).order_by('-id')
        context['leave_application_history'] = leave_application_histroy

        if EmployeeDesignation.objects.filter(employee_id=obj.supervisor, isActive=True).exists():
            context['permission'] = True

        else:
            context['permission'] = False


        if request.method == "POST":

            startDate = datetime.strptime(request.POST['start_date'], "%Y/%m/%d")
            endDate = datetime.strptime(request.POST['hidden_to_date'], "%Y/%m/%d")
            dayCount = abs(endDate - startDate).days + 1
            totalDays = dayCount
            checkDate = startDate
            duplicate_check = False
            balance_check = False
            confirmed_by = request.POST['hiddhen_confirmed_by']
            message = {}

            weekend_list = WeeklyHoliday.objects.filter(isActive=True)
            holiday_list = YearlyHoliday.objects.filter(date__range=(startDate,endDate))

            leave_type = get_object_or_404(LeaveCategory,pk=request.POST['type'])
            try:

                leave_balance_obj = LeaveAllotment.objects.filter(isActive=True, employee_id=request.user.employeeuser.employee_id, leave_id__type__id = leave_type.id, year = startDate.year).latest('id')
                leave_balance = leave_balance_obj.balance
            except ObjectDoesNotExist:

                joining_date = obj.employee_id.joiningDate.year
                if joining_date == date.today().year :
                    leave_balance = round((leave_type.amount / 365) * (365 - obj.employee_id.joiningDate.timetuple().tm_yday))
                else:
                    leave_balance = leave_type.amount



            for d in range(0,dayCount):
                if WeeklyHoliday.objects.filter(effectiveFrom__lte=checkDate, effectiveEnd__gte=checkDate, dayNum=checkDate.isoweekday()).exists() or YearlyHoliday.objects.filter(date=checkDate).exists():
                    totalDays = totalDays - 1
                '''for weekend in weekend_list:
                    if checkDate.isoweekday() == weekend.dayNum:
                        totalDays = totalDays - 1
                      #  print(checkDate.date())
                       # print(totalDays)
                        break


                for holiday in holiday_list:
                    if checkDate.date() == holiday.date:
                        totalDays = totalDays - 1
                      #  print(checkDate.date())
                      #  print(totalDays)
                        break
                '''
                if LeaveHistory.objects.filter(employee_id=request.user.employeeuser.employee, date_from__lte=checkDate, date_to__gte=checkDate, isActive=True).exists():
                    duplicate_check = True
                    message = 'duplicate'

                checkDate = checkDate + timedelta(days=1)

            if totalDays > leave_balance:
                balance_check = True


            if (totalDays == int(request.POST['amount'])) and (duplicate_check == False) and (balance_check == False):
                if confirmed_by != '0':
                    leave_obj = LeaveHistory(date_from = startDate,
                                             date_to = endDate,
                                             count = totalDays,
                                             employee_id = obj.employee_id,
                                             endorsed_by = obj.supervisor,
                                             confirmed_by_id = confirmed_by,
                                             type = get_object_or_404(LeaveCategory,pk=request.POST['type']),
                                             endorsement = '0',
                                             isActive = True,
                                             description = request.POST['reason'],
                                             insertUser = request.user.id,
                                             insertDate = date.today())
                    leave_obj.save()

                else:
                    leave_obj = LeaveHistory(date_from = startDate,
                                             date_to = endDate,
                                             count = totalDays,
                                             employee_id = obj.employee_id,
                                             endorsed_by = obj.supervisor,
                                             type = get_object_or_404(LeaveCategory,pk=request.POST['type']),
                                             endorsement = '0',
                                             isActive = True,
                                             description = request.POST['reason'],
                                             insertUser = request.user.id,
                                             insertDate = date.today())
                    leave_obj.save()

                dayCount = abs(endDate - startDate).days + 1
                totalDays = dayCount
                dateValue = startDate

                for count in range(0,dayCount):
                    if (YearlyHoliday.objects.filter(date=dateValue).exists() == False) and  (WeeklyHoliday.objects.filter(effectiveFrom__lte=dateValue, effectiveEnd__gte=dateValue, dayNum=dateValue.isoweekday()).exists() == False):
                        new_leave_details_object = LeaveDetail(date = dateValue,
                                                               isActive = True,
                                                               leave_id = leave_obj,
                                                               insertUser = request.user.id,
                                                               insertDate = date.today())
                        new_leave_details_object.save()

                    dateValue = dateValue + timedelta(days=1)

                try:
                    leave_balance = LeaveAllotment.objects.filter(isActive=True, employee_id=leave_obj.employee_id, leave_id__type__id = leave_obj.type_id, year = leave_obj.date_from.year).latest('id')

                    new_balance = leave_balance.balance - leave_obj.count
                    leave_balance.updateUser = request.user.id
                    leave_balance.updateDate = date.today()
                    leave_balance.save()
                    new_leave_balance_obj = LeaveAllotment(balance = new_balance,
                                                           employee_id = leave_obj.employee_id,
                                                           leave_id = leave_obj,
                                                           isActive = True,
                                                           year = leave_obj.date_from.year,
                                                           insertUser = request.user.id,
                                                           insertDate = date.today(),
                                                           insertType = 'insert',
                                                           project = '1'
                                                           )

                    new_leave_balance_obj.save()
                except ObjectDoesNotExist:
                    if leave_obj.employee_id.joiningDate.year == date.today().year:
                        allocated_balance = round((leave_obj.type.amount / 365) * (365 - leave_obj.employee_id.joiningDate.timetuple().tm_yday))
                        new_balance = allocated_balance - leave_obj.count
                    else:
                        new_balance = leave_obj.type.amount - leave_obj.count

                    new_leave_balance_obj = LeaveAllotment(balance = new_balance,
                                                           employee_id = leave_obj.employee_id,
                                                           leave_id = leave_obj,
                                                           isActive = True,
                                                           year = leave_obj.date_from.year,
                                                           insertUser = request.user.id,
                                                           insertDate = date.today(),
                                                           insertType = 'insert',
                                                           project = '1')
                    new_leave_balance_obj.save()


                message = 'applied'

            elif balance_check == True:
                message = 'extra'

            elif duplicate_check == True:
                message = 'duplicate'
            else:
                message = 'miscount'

            return redirect('leave:applyLeave', message=message)

        pending_list = LeaveHistory.objects.filter(employee_id=obj.employee_id, endorsement='0' )
        context['pending_list'] = pending_list

        if message == 'add':
            context['form_message'] = ''
        elif message == 'extra':
            context['form_message'] = 'You cannot apply for more days than your balance'
        elif message == 'duplicate':
            context['form_message'] = 'Duplicate Entry!! Already Applied for the date'
        elif message == 'applied':
            context['form_message'] = 'Leave Application is submitted successfully to ' + obj.supervisor.get_gender_display() + ' ' + obj.supervisor.employeeName
        elif message == 'miscount':
            context['form_message'] = 'Day Calculation is not Correct'
        else:
            context['form_message'] = 'Some error Occured'


    except ObjectDoesNotExist:
        context['error_message'] = '!!!  This page is for Employee  !!!'


    return render(request, 'leave/applyLeave.html', context)


@login_required
def pendingApplication(request):

    context = {}
    try:
        pending_application_list = LeaveHistory.objects.filter(endorsed_by = request.user.employeeuser.employee, endorsement='0', isActive=True)
        context['pending_application_list'] = pending_application_list
        pending_confirmation_list = LeaveHistory.objects.filter(confirmed_by = request.user.employeeuser.employee, endorsement='3', isActive=True)
        context['pending_confirmation_list'] = pending_confirmation_list
    except:
        context['error_message'] = '!!! This page is for Employee !!!'

    return render(request, 'leave/leaveApplication.html',context)


@login_required
def applicationApproval(request, leave_id, status):

    obj = LeaveHistory.objects.get(pk=leave_id)
    if status == 'approved':

        '''
        try:
            leave_balance = LeaveAllotment.objects.filter(isActive=True, employee_id=obj.employee_id, leave_id__type__id = obj.type_id, year = obj.date_from.year).latest('id')

            new_balance = leave_balance.balance - obj.count
            leave_balance.updateUser = request.user.id
            leave_balance.updateDate = date.today()
            leave_balance.save()
            new_leave_balance_obj = LeaveAllotment(balance = new_balance,
                                                   employee_id = obj.employee_id,
                                                   leave_id = obj,
                                                   isActive = True,
                                                   year = obj.date_from.year,
                                                   insertUser = request.user.id,
                                                   insertDate = date.today()
                                                   )

            new_leave_balance_obj.save()
        except ObjectDoesNotExist:
            if obj.employee_id.joiningDate.year == date.today().year:
                allocated_balance = round((obj.type.amount / 365) * (365 - obj.employee_id.joiningDate.timetuple().tm_yday))
                new_balance = allocated_balance - obj.count
            else:
                new_balance = obj.type.amount - obj.count

            new_leave_balance_obj = LeaveAllotment(balance = new_balance,
                                                   employee_id = obj.employee_id,
                                                   leave_id = obj,
                                                   isActive = True,
                                                   year = obj.date_from.year,
                                                   insertUser = request.user.id,
                                                   insertDate = date.today())
            new_leave_balance_obj.save()
        '''
        if obj.endorsement == '3':
            obj.endorsement = '1'

        elif (obj.confirmed_by != None) and (obj.endorsed_by != obj.confirmed_by):
            obj.endorsement = '3'
        else:
            obj.endorsement = '1'

        obj.updateUser = request.user.id
        obj.updateDate = date.today()

        obj.save()
        '''
        startDate = obj.date_from
        endDate = obj.date_to
        dayCount = abs(endDate - startDate).days + 1
        totalDays = dayCount
        dateValue = startDate

        for count in range(0,dayCount):
            if (YearlyHoliday.objects.filter(date=dateValue).exists() == False) and  (WeeklyHoliday.objects.filter(isActive=True, dayNum=dateValue.isoweekday()).exists() == False):
                new_leave_details_object = LeaveDetail(date = dateValue,
                                                       isActive = True,
                                                       leave_id = obj,
                                                       insertUser = request.user.id,
                                                       insertDate = date.today())
                new_leave_details_object.save()

            dateValue = dateValue + timedelta(days=1)
        '''

    elif status == 'reject':
        obj.endorsement = '2'
        obj.updateUser = request.user.id
        obj.updateDate = date.today()
        obj.save()

        leave_balance = LeaveAllotment.objects.get(leave_id = obj)

        latest_leave_balance = LeaveAllotment.objects.filter(isActive=True, employee_id=obj.employee_id, leave_id__type__id = obj.type_id, year = obj.date_from.year).latest('id')

        if leave_balance == latest_leave_balance:
            leave_balance.delete()
        else:
            day_count = leave_balance.leave_id.count
            leave_balance.delete()
            try:
                new_leave_balance = LeaveAllotment.objects.filter(isActive=True, employee_id=obj.employee_id, leave_id__type__id = obj.type_id, year = obj.date_from.year).latest('id')
                new_leave_balance.balance += day_count
                new_leave_balance.updateUser = request.user.id
                new_leave_balance.updateDate = date.today()
                new_leave_balance.save()
            except ObjectDoesNotExist:
                pass


    return HttpResponseRedirect(reverse('leave:pendingApplication'))


@login_required
def admin_leave_page(request):

    context = {}

    active_employee_list = Employee.objects.filter(isActive=True).order_by('employeeName')
    context['active_employee_list'] = active_employee_list

    if request.method == "POST":

        category = request.POST['category']
        start_date = datetime.strptime(request.POST['startDate'], "%Y/%m/%d")
        end_date = datetime.strptime(request.POST['endDate'], "%Y/%m/%d")


        if 'all_employee' in request.POST:

            if category == 'leave':
                active_list = LeaveHistory.objects.filter(isActive=True, date_from__gte=start_date, date_to__lte=end_date).order_by('employee_id__employeeName')
                #context['active_leave_list'] = active_leave_list
                #context['active_sms_list'] = active_sms_list

                paginator = Paginator(active_list, 100)

                page = request.GET.get('page')

                try:
                    contacts = paginator.page(page)
                except PageNotAnInteger:
                    contacts = paginator.page(1)
                except EmptyPage:
                    contacts = paginator.page(paginator.num_pages)

                context['leave_contacts'] = contacts

            elif category == 'sms':
                end_date = end_date + timedelta(days=1)
                active_list = Late.objects.filter(date__gte=start_date, date__lte=end_date).order_by('-date')

                #context['active_leave_list'] = active_leave_list
                #context['active_sms_list'] = active_sms_list

                paginator = Paginator(active_list, 100)

                page = request.GET.get('page')

                try:
                    contacts = paginator.page(page)
                except PageNotAnInteger:
                    contacts = paginator.page(1)
                except EmptyPage:
                    contacts = paginator.page(paginator.num_pages)

                context['contacts'] = contacts

        else:
            if category == 'leave':
                active_list = LeaveHistory.objects.filter(isActive=True, employee_id_id = request.POST['emp_id'], date_from__gte=start_date, date_to__lte=end_date).order_by('employee_id__employeeName')
                #context['active_leave_list'] = active_leave_list
                #context['active_sms_list'] = active_sms_list

                paginator = Paginator(active_list, 100)

                page = request.GET.get('page')

                try:
                    contacts = paginator.page(page)
                except PageNotAnInteger:
                    contacts = paginator.page(1)
                except EmptyPage:
                    contacts = paginator.page(paginator.num_pages)

                context['leave_contacts'] = contacts

            elif category == 'sms':
                end_date = end_date + timedelta(days=1)
                active_list = Late.objects.filter(isActive=True, emp_id_id= request.POST['emp_id'], date__gte=start_date, date__lte=end_date).order_by('-date')

                #context['active_leave_list'] = active_leave_list
                #context['active_sms_list'] = active_sms_list

                paginator = Paginator(active_list, 100)

                page = request.GET.get('page')

                try:
                    contacts = paginator.page(page)
                except PageNotAnInteger:
                    contacts = paginator.page(1)
                except EmptyPage:
                    contacts = paginator.page(paginator.num_pages)

                context['contacts'] = contacts



    return  render(request, 'leave/admin_leave_page.html', context)


@login_required
def admin_approval_modification(request):

    context = {}

    active_leave_list = LeaveHistory.objects.filter(isActive=True).order_by('employee_id__employeeName')
    active_sms_list = Late.objects.filter(isActive=True).order_by('-date')
    context['active_leave_list'] = active_leave_list
    context['active_sms_list'] = active_sms_list
    return  render(request, 'leave/admin_approval_modification_new.html', context)

@login_required
def admin_leave_edit(request, leave_id, request_type):

    try:
        leave_obj = LeaveHistory.objects.get(id=leave_id)

        if request_type == 'reverse':
            if leave_obj.endorsement == '2':
                try:
                    leave_balance = LeaveAllotment.objects.filter(isActive=True, employee_id=leave_obj.employee_id, leave_id__type__id = leave_obj.type_id, year = leave_obj.date_from.year).latest('id')

                    new_balance = leave_balance.balance - leave_obj.count
                    leave_balance.updateUser = request.user.id
                    leave_balance.updateDate = date.today()
                    leave_balance.save()
                    new_leave_balance_obj = LeaveAllotment(balance = new_balance,
                                                           employee_id = leave_obj.employee_id,
                                                           leave_id = leave_obj,
                                                           isActive = True,
                                                           year = leave_obj.date_from.year,
                                                           insertUser = request.user.id,
                                                           insertDate = date.today(),
                                                           insertType = 'reverse',
                                                           project = '1'
                                                           )

                    new_leave_balance_obj.save()
                except ObjectDoesNotExist:
                    if leave_obj.employee_id.joiningDate.year == date.today().year:
                        allocated_balance = round((leave_obj.type.amount / 365) * (365 - leave_obj.employee_id.joiningDate.timetuple().tm_yday))
                        new_balance = allocated_balance - leave_obj.count
                    else:
                        new_balance = leave_obj.type.amount - leave_obj.count

                    new_leave_balance_obj = LeaveAllotment(balance = new_balance,
                                                           employee_id = leave_obj.employee_id,
                                                           leave_id = leave_obj,
                                                           isActive = True,
                                                           year = leave_obj.date_from.year,
                                                           insertUser = request.user.id,
                                                           insertDate = date.today(),
                                                           insertType = 'reverse',
                                                           project = '1')
                    new_leave_balance_obj.save()

            leave_obj.endorsement = '0'
            leave_obj.updateUser = request.user.id
            leave_obj.updateDate = date.today()
            leave_obj.save()

        elif request_type == 'delete':
            leave_obj.isActive = False
            leave_obj.isDelete = True
            leave_obj.updateDate = date.today()
            leave_obj.updateUser = request.user.id
            leave_obj.save()

            leave_detail_obj_list = LeaveDetail.objects.filter(leave_id=leave_obj)

            for list in leave_detail_obj_list:
                list.isActive = False
                list.isDelete = True
                list.updateDate = date.today()
                list.updateUser = request.user.id
                list.save()

            try:
                leave_balance = LeaveAllotment.objects.get(leave_id = leave_obj)

                latest_leave_balance = LeaveAllotment.objects.filter(isActive=True, employee_id=leave_obj.employee_id, leave_id__type__id = leave_obj.type_id, year = leave_obj.date_from.year).latest('id')

                if leave_balance == latest_leave_balance:
                    leave_balance.delete()

                else:
                    day_count = leave_balance.leave_id.count
                    leave_balance.delete()

                    try:
                        new_leave_balance = LeaveAllotment.objects.filter(isActive=True, employee_id=leave_obj.employee_id, leave_id__type__id = leave_obj.type_id, year = leave_obj.date_from.year).latest('id')
                        new_leave_balance.balance += day_count
                        new_leave_balance.updateUser = request.user.id
                        new_leave_balance.updateDate = date.today()
                        new_leave_balance.save()

                    except ObjectDoesNotExist:
                        pass
            except ObjectDoesNotExist:
                pass

        

    except ObjectDoesNotExist:
        error_message = 'Object does not exits'

    return HttpResponseRedirect(reverse('leave:admin_leave_page'))


@login_required
def admin_attendance_sms_edit(request, sms_id, request_type):


    try:
        sms_obj = Late.objects.get(id=sms_id)

        if request_type == 'delete':
            sms_obj.isActive = False
            sms_obj.isDelete = True
            sms_obj.save()

        elif request_type == 'reverse':
            sms_obj.isEndorsed = '0'
            sms_obj.save()

    except ObjectDoesNotExist:
        error_message = 'Object does not exits'

    return HttpResponseRedirect(reverse('leave:admin_leave_page'))

@login_required
def leave_print(request, leave_id):

    '''from reportlab.pdfbase import pdfdoc

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")
    pdfdoc.PDFCatalog.OpenAction = '<</S/JavaScript/JS(this.print\({bUI:true,bSilent:false,bShrinkToFit:true}\);)>>'

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response
        '''
    context = {}
    policy = True

    try:
        leave_obj = LeaveHistory.objects.get(id=int(leave_id))
        employee_obj = EmployeeDesignation.objects.get(employee_id=leave_obj.employee_id, isActive=True)
        balance_list = {}
        balance_remain = 0
        endorsement_count = 0
        pending_count = 0
        leave_category_obj = LeaveCategory.objects.get(id=leave_obj.type_id)
        allocated_balance = leave_category_obj.amount


        if policy:

            joining_date = employee_obj.employee_id.joiningDate.year
            if joining_date == leave_obj.date_from.year :
                try:
                    allocated_balance = round((leave_category_obj.amount / 365) * (365 - leave_category_obj.employee_id.joiningDate.timetuple().tm_yday))

                except:
                    error_message ="Incomplete Employee Info. \n No Joining Date!!!"
                    context['joining_date_null_error'] = error_message
                    allocated_balance = 0

            leave_history_list = LeaveHistory.objects.filter(employee_id=employee_obj.employee_id, isActive=True, date_from__year=leave_obj.date_from.year, date_to__year=leave_obj.date_from.year, type=leave_obj.type, id__lt=leave_obj.id)

            for list in leave_history_list:
                if list.endorsement == '1':
                    endorsement_count += list.count

                elif list.endorsement == '0':
                    pending_count += list.count

            '''
            if leave_obj.endorsement == '1':
                endorsement_count = endorsement_count - leave_obj.count

            elif leave_obj.endorsement == '0':
                pending_count = pending_count - leave_obj.count




            try:
                leave_balance = LeaveAllotment.objects.get(leave_id__type__id = leave_category_obj.id, isActive=True, employee_id=employee_obj.employee_id, year=leave_obj.date_from.year)
                balance_remain = leave_balance.balance

            except ObjectDoesNotExist:
                balance_remain = allocated_balance
                '''

        context['entitled'] = allocated_balance
        context['taken'] = endorsement_count
        context['applied_for'] = leave_obj.count
        context['pending'] = pending_count
        context['balance'] = allocated_balance - (endorsement_count + leave_obj.count + pending_count)



    except:
        pass

    context['leave_obj'] = leave_obj
    context['emp_obj'] = employee_obj
    context['balance_list'] = balance_list

    return render(request, 'leave/leave_print_page.html',context)