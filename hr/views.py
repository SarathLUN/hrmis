from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Employee, Department, DepartmentDetails, Designation, EmployeeDesignation, Location
from django.template import loader,RequestContext
from django.core.urlresolvers import reverse
from datetime import date, datetime, timedelta,timezone
from .custom_functions import populateMessage
from django.contrib.auth.decorators import login_required
from django.db import connection,transaction
from HRM.myScript import convert_to_date
from django.core.exceptions import ObjectDoesNotExist
from leave.models import LeaveHistory
from django.contrib import messages

# Create your views here.

@login_required
def index(request):
    context = {}
    template = loader.get_template('hr/index.html')
    time = datetime.now(timezone.utc)
    context['time'] = time
    return render(request, 'home.html',context)


'''
start:: addEmployeePage
    author: Tusfiqur Alam
    // rendered to hr/addEmployee.html,
    // values sent in context are all the objects of Employee, Department, Location, Designation & EmployeeDesignation models
'''

@login_required
def addEmployeePage(request, message):
    context = {}
    if message == 'True':
        context['form_message'] = 'NEW EMPLOYEE HAS BEEN ADDED SUCCESSFULLY!!'
    elif message == 'False':
        context['form_message'] = 'Duplicated Entry for Card Id. Already exists!!!'
    else:
        context['form_message'] = ''

    employee_list = Employee.objects.all().order_by('employeeName')
    department_list = Department.objects.all().order_by('departmentName')
    location_list = Location.objects.all().order_by('locationName')
    designation_list = Designation.objects.all().order_by('designation')
    emp_des_list = EmployeeDesignation.objects.all()

    context['employee_list'] = employee_list
    context['department_list'] = department_list
    context['location_list'] = location_list
    context['designation_list'] = designation_list

    return render(request, 'hr/addEmployee.html', context)

'''
end:: addEmployeePage
    author: Tusfiqur Alam
    // rendered to hr/addEmployee.html,
    // values sent in context are all the objects of Employee, Department, Location, Designation & EmployeeDesignation models
'''


@login_required
def addEmployeePerfomed(request):

    date_of_birth = convert_to_date(request.POST['dateOfBirth'])
    joining_date = convert_to_date(request.POST['joiningDate'])

    '''e = Employee(employeeName = request.POST['employeeName'],
                 gender = request.POST['title'],
                 presentAddress = request.POST['presentAddress'],
                 permanentAddress = request.POST['permanentAddress'],
                 fatherName = request.POST['fatherName'],
                 motherName = request.POST['motherName'],
                 email = request.POST['email'],
                 bloodGroup = request.POST['bloodGroup'],
                 nationality = request.POST['nationality'],
                 nationalId = request.POST['nationalId'],
                 joiningDate = joining_date,
                 dateOfBirth = date_of_birth,
                 passportId = request.POST['passportId'],
                 employeeCode = request.POST['employeeCode'],
                 cardId = request.POST['cardId'],
                 bankName = request.POST['bankName'],
                 bankAccountNo = request.POST['bankAccountNo'],
                 mobile = request.POST['mobile'],
                 isActive = True,
                 isDelete = False,
                 insertUser=request.user.id,
                 insertDate=date.today(),
                 project='1')
    e.save()

    '''

    emp_obj, created = Employee.objects.get_or_create(cardId = request.POST['cardId'],
                                                      defaults={'employeeName' : request.POST['employeeName'],
                                                                'gender' : request.POST['title'],
                                                                'presentAddress' : request.POST['presentAddress'],
                                                                'permanentAddress' : request.POST['permanentAddress'],
                                                                'fatherName' : request.POST['fatherName'],
                                                                'motherName' : request.POST['motherName'],
                                                                'email' : request.POST['email'],
                                                                'bloodGroup' : request.POST['bloodGroup'],
                                                                'nationality' : request.POST['nationality'],
                                                                'nationalId' : request.POST['nationalId'],
                                                                'joiningDate' : joining_date,
                                                                'dateOfBirth' : date_of_birth,
                                                                'passportId' : request.POST['passportId'],
                                                                'employeeCode' : request.POST['employeeCode'],
                                                                'bankName' : request.POST['bankName'],
                                                                'bankAccountNo' : request.POST['bankAccountNo'],
                                                                'mobile' : request.POST['mobile'],
                                                                'isActive' : True,
                                                                'isDelete' : False,
                                                                'insertUser' : request.user.id,
                                                                'insertDate' : date.today(),
                                                                'project' : '1'
                                                      })

    if created:

        if request.POST['date'] != '':
            effective_start_date = convert_to_date(request.POST['date'])
            obj = EmployeeDesignation(employee_id = get_object_or_404(Employee, pk=emp_obj.employee_id),
                                      department_id = get_object_or_404(Department,pk=request.POST['departmentId']),
                                      des_id = get_object_or_404(Designation, pk=request.POST['designationId']),
                                      location_id = get_object_or_404(Location, pk=request.POST['locationId']),
                                      effective_date_start = effective_start_date,
                                      supervisor = get_object_or_404(Employee, pk=request.POST['supervisor']),
                                      isActive = True,
                                      insertUser=request.user.id,
                                      insertDate=date.today(),
                                      project='1')
            obj.save()

        context = { 'employeeId' : emp_obj.employee_id, }
    #print(e.employee_id)
    return redirect('hr:addEmployeePage', message=created)


@login_required
def viewEmployeeList(request, message):
    emp_list = Employee.objects.all().order_by('employeeName')
    context = {}
    context['employee_list'] = emp_list
    if message == 'edited':
        context['form_message'] = "EDITED & STORED SUCCESSFULLY!!"
    else:
        context['form_message'] = ''


    cursor = connection.cursor()
    cursor.execute("select hr_employee.employee_id, hr_employee.employeeName, hr_employee.cardId, ifnull(dept, 'Not Assigned') as dept from hr_employee left join ( select hr_employeedesignation.*, hr_department.departmentName as dept from hr_department left join hr_employeedesignation on hr_employeedesignation.isActive=TRUE and hr_employeedesignation.department_id_id=hr_department.department_id) as ed1 on hr_employee.employee_id = ed1.employee_id_id order by hr_employee.employeeName")
    row = cursor.fetchall()

    ''' for r in row:
        print(r)
    '''
    context['row'] = row

    return render(request, 'hr/employeeListPage.html', context)


@login_required
def editEmployee(request, employee_id):
    obj = get_object_or_404(Employee,pk=employee_id)
    context = {}
    context['employee'] = obj

    return render(request, 'hr/editEmployeePage.html', context)


@login_required
def editEmployeePerfomed(request, employee_id):

    date_of_birth = convert_to_date(request.POST['dateOfBirth'])
    joining_date = convert_to_date(request.POST['joiningDate'])

    emp = get_object_or_404(Employee, pk=employee_id)
    emp.gender = request.POST['title']
    emp.employeeName = request.POST['employeeName']
    emp.mobile = request.POST['mobile']
    emp.fatherName = request.POST['fatherName']
    emp.motherName = request.POST['motherName']
    emp.dateOfBirth = date_of_birth
    emp.bloodGroup = request.POST['bloodGroup']
    emp.nationality = request.POST['nationality']
    emp.nationalId = request.POST['nationalId']
    emp.passportId = request.POST['passportId']
    emp.employeeCode = request.POST['employeeCode']
    emp.cardId = request.POST['cardId']
    emp.joiningDate = joining_date
    emp.bankName = request.POST['bankName']
    emp.bankAccountNo = request.POST['bankAccountNo']
    emp.email = request.POST['email']
    emp.permanentAddress = request.POST['permanentAddress']
    emp.presentAddress = request.POST['presentAddress']
    emp.updateUser = request.user.id
    emp.updateDate = date.today()

    emp.save()

    return redirect('hr:viewEmployeeList', 'edited')


@login_required
def addDepartmentPage(request,message):
    department_list = Department.objects.all().order_by('departmentName')
    context = {}
    context['department_list'] = department_list
    context['form_message'] = populateMessage(message)

    return render(request, 'hr/addDepartment.html', context)


@login_required
def addDepartmentPerfomed(request):

    obj,created = Department.objects.get_or_create(departmentName = request.POST['departmentName'],
                                           defaults={'description' : request.POST['location'],
                                                     'isActive' : True,
                                                     'isDelete' : False,
                                                     'insertUser' : request.user.id,
                                                     'insertDate' : date.today(),
                                                     'project' : '1'})


    return redirect('hr:addDepartmentPage', message=created)


@login_required
def editDepartmentPerformed(request,dept_id):
    dept = get_object_or_404(Department, pk=dept_id)
    dept.departmentName = request.POST['departmentName']
    dept.description = request.POST['location']
    dept.updateUser = request.user.id
    dept.updateDate = date.today()

    dept.save()
    return redirect('hr:addDepartmentPage', message='edited')


@login_required
def addDesignation(request,message):
    designation_list = Designation.objects.all().order_by('designation')
    context = {}
    context['designation_list'] = designation_list
    context['form_message'] = populateMessage(message)

    return render(request, 'hr/addDesignation.html', context)


@login_required
def addDesingationPerfomed(request):

    obj, created = Designation.objects.get_or_create(designation = request.POST['designationName'],
                                                     defaults={'desCode' : request.POST['designationCode'],
                                                               'isActive' : True,
                                                               'isDelete' : False,
                                                               'insertUser' : request.user.id,
                                                               'insertDate' : date.today(),
                                                               'project' : '1'})

    return redirect('hr:addDesignationPage', message=created)


@login_required
def editDesignationPerfomed(request, des_id):
    des = get_object_or_404(Designation, pk=des_id)
    des.designation = request.POST['designationName']
    des.desCode = request.POST['designationCode']
    des.updateUser = request.user.id
    des.updateDate = date.today()
    des.save()

    return redirect('hr:addDesignationPage', message='edited')


@login_required
def addLocationPage(request,message):
    location_list = Location.objects.all().order_by('locationName')
    context = {}
    context['location_list'] = location_list
    context['form_message'] = populateMessage(message)

    return render(request, 'hr/addLocation.html', context)


@login_required
def addLocationPerfomed(request):
    obj, created = Location.objects.get_or_create(locationName = request.POST['locationName'],
                                         defaults={'locationCode' : request.POST['locationCode'],
                                                   'description' : request.POST['description'],
                                                   'isActive' : True,
                                                   'isDelete' : False,
                                                   'insertUser' : request.user.id,
                                                   'insertDate' : date.today(),
                                                   'project' : '1'})

    return redirect('hr:addLocationPage', message=created)


@login_required
def editLocationPerfomed(request, loc_id):
    loc = get_object_or_404(Location, pk=loc_id)
    loc.locationName = request.POST['locationName']
    loc.locationCode = request.POST['locationCode']
    loc.description = request.POST['description']
    loc.updateUser = request.user.id
    loc.updateDate = date.today()

    loc.save()

    return redirect('hr:addLocationPage', message='edited')


@login_required
def addEmployeeDesignationPage(request):

    if request.is_ajax():
        data = {}
        emp_des_id = request.POST.get('emp_des_id')
        emp_id = EmployeeDesignation.objects.get(emp_des_id=emp_des_id)

        if LeaveHistory.objects.filter(endorsement__in=['0','3'], endorsed_by_id=emp_id.employee_id_id).exists():
            data['alert'] = "pending"


        return JsonResponse(data)

    supervisor_list = Employee.objects.all().order_by('employeeName')
    employee_list = Employee.objects.filter(employee=None).order_by('employeeName')
    department_list = Department.objects.all().order_by('departmentName')
    location_list = Location.objects.all().order_by('locationName')
    designation_list = Designation.objects.all().order_by('designation')
    emp_des_list = EmployeeDesignation.objects.filter(isActive=True).order_by('department_id__departmentName','employee_id__employeeName')


    context = {'employee_list' : employee_list,
               'department_list' : department_list,
               'location_list' : location_list,
               'designation_list' : designation_list,
               'emp_des_list' : emp_des_list,
               'supervisor_list': supervisor_list}

    return render(request, 'hr/addEmployeeDesignation.html', context)


@login_required
def addEmployeeDesignationPerfomed(request):
    effective_start_date = convert_to_date(request.POST['date'])
    obj = EmployeeDesignation(employee_id = get_object_or_404(Employee, pk=request.POST['employeeId']),
                              department_id = get_object_or_404(Department,pk=request.POST['departmentId']),
                              des_id = get_object_or_404(Designation, pk=request.POST['designationId']),
                              location_id = get_object_or_404(Location, pk=request.POST['locationId']),
                              effective_date_start = effective_start_date,
                              effective_date_end = datetime.max.date(),
                              supervisor = get_object_or_404(Employee, pk=request.POST['supervisor']),
                              isActive = True,
                              isDelete = False,
                              insertUser = request.user.id,
                              insertDate = date.today(),
                              project = '1',
                              status='new'
                              )
    obj.save()


    return HttpResponseRedirect(reverse('hr:addEmployeeDesignationPage'))


@login_required
def editEmployeeDesignation_admin(request):


    if request.is_ajax():
        pk=request.POST.get('pk')
        return JsonResponse()

    supervisor_list = Employee.objects.all().order_by('employeeName')
    employee_list = Employee.objects.filter(employee=None).order_by('employeeName')
    department_list = Department.objects.all().order_by('departmentName')
    location_list = Location.objects.all().order_by('locationName')
    designation_list = Designation.objects.all().order_by('designation')
    emp_des_list = EmployeeDesignation.objects.all().order_by('department_id__departmentName','employee_id__employeeName')
    #print(supervisor_list.count())
    #print(employee_list.count())

    context = {'employee_list' : employee_list,
               'department_list' : department_list,
               'location_list' : location_list,
               'designation_list' : designation_list,
               'emp_des_list' : emp_des_list,
               'supervisor_list': supervisor_list}


    return render(request, 'hr/editEmployeeDesignation.html', context)


@login_required
def editEmployee_admin(request, emp_des_id):

    new_effective_date_start = convert_to_date(request.POST['date'])
    print(request.POST['isActive'])

    des_obj = get_object_or_404(EmployeeDesignation, pk=emp_des_id)
    des_obj.department_id = get_object_or_404(Department, pk=request.POST['departmentId'])
    des_obj.des_id = get_object_or_404(Designation, pk=request.POST['designationId'])
    des_obj.location_id = get_object_or_404(Location, pk=request.POST['locationId'])
    des_obj.supervisor_id = int(request.POST['supervisor'])
    des_obj.effective_date_start = new_effective_date_start
    des_obj.updateUser = request.user.id
    des_obj.updateDate = date.today()
    des_obj.status = request.POST['status']
    des_obj.isActive = request.POST['isActive']
    des_obj.save()


    return HttpResponseRedirect(reverse('hr:editEmployeeDesignationPage'))



@login_required
def editEmployeeDesignationPerfomed(request, emp_des_id):

    new_effective_date_start = convert_to_date(request.POST['date'])
    old_effective_date_end =new_effective_date_start - timedelta(days=1)

    reason_status = request.POST['reason']
    employee_obj = get_object_or_404(EmployeeDesignation, pk=emp_des_id)
    #end_date = convert_to_date(request.POST['end_date'])

    # old_obj, created = EmployeeDesignation.objects.get_or_create(employee_id)


    if reason_status in ("left", "terminated"):

        if (LeaveHistory.objects.filter(endorsement='0', endorsed_by_id=employee_obj.employee_id_id, isActive=True).exists() | LeaveHistory.objects.filter(endorsement='3', confirmed_by=employee_obj.employee_id_id, isActive=True).exists()):
            messages.add_message(request,messages.ERROR, 'THIS EMPLOYEE HAS PENDING APPROVAL ISSUE. CANNOT PERFORM THE CHANGE!!')
            return HttpResponseRedirect(reverse('hr:addEmployeeDesignationPage'))
        else:
            try:
                to_update = EmployeeDesignation.objects.get(emp_des_id=emp_des_id)
                to_update.effective_date_end = new_effective_date_start
                to_update.isActive = False
                to_update.status = reason_status
                to_update.updateUser = request.user.id
                to_update.updateDate = date.today()

                to_update.save()

            except ObjectDoesNotExist:
                message = "No object Found"

    else:

        des_obj, created = EmployeeDesignation.objects.get_or_create(employee_id = get_object_or_404(Employee, pk=request.POST['hidden_emp_id']),
                                                                     department_id = get_object_or_404(Department,pk=request.POST['departmentId']),
                                                                     des_id = get_object_or_404(Designation, pk=request.POST['designationId']),
                                                                     location_id = get_object_or_404(Location, pk=request.POST['locationId']),
                                                                     effective_date_start = new_effective_date_start,
                                                                     supervisor = get_object_or_404(Employee, pk=request.POST['supervisor']),
                                                                     isActive = True,
                                                                     status = reason_status,
                                                                     defaults={
                                                                         'effective_date_end' : datetime.max.date(),
                                                                         'insertUser' : request.user.id,
                                                                         'insertDate' : date.today(),
                                                                         'project' : '1',
                                                                     }
                                                                     )

        if created:
            obj = get_object_or_404(EmployeeDesignation, pk=emp_des_id)
            obj.updateUser = request.user.id
            obj.updateDate = date.today()
            obj.effective_date_end = old_effective_date_end
            obj.isActive = False
            #obj.status = reason_status

            obj.save()

    '''
    new_emp_des_obj = EmployeeDesignation(employee_id = get_object_or_404(Employee, pk=request.POST['hidden_emp_id']),
                                          department_id = get_object_or_404(Department,pk=request.POST['departmentId']),
                                          des_id = get_object_or_404(Designation, pk=request.POST['designationId']),
                                          location_id = get_object_or_404(Location, pk=request.POST['locationId']),
                                          effective_date_start = new_effective_date_start,
                                          effective_date_end = datetime.max.date(),
                                          supervisor = get_object_or_404(Employee, pk=request.POST['supervisor']),
                                          isActive = True,
                                          insertUser = request.user.id,
                                          insertDate = date.today(),
                                          project = '1')
    new_emp_des_obj.save()
    '''
    return HttpResponseRedirect(reverse('hr:addEmployeeDesignationPage'))


