from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password,make_password
from django.contrib.auth.models import User
from hr.models import Employee
from datetime import date, datetime, timedelta
from .models import EmployeeUser,MenuTable,GroupTable, UserGroupTable, MenuGroupTable
from django.http import JsonResponse
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from holiday.models import YearlyHoliday

# Create your views here.


@login_required
def password_change(request):

    context = {}
    if request.method == 'POST':
        if request.user.check_password(request.POST['current_password']):
            request.user.set_password(request.POST['new_password'])
            request.user.save()


            context['message'] = 'Password has been reset'
        else:
            context['message'] = 'Current Password is incorrect'
    return render(request, 'account/passwordChange.html', context)

@login_required
def create_employee_user(request):

    context = {}
    #employee_list_all = Employee.objects.all()

    if request.method == 'POST':
        group_id = request.POST['group']
        new_user = User(username=request.POST['username'],
                        password=request.POST['password'],
                        is_superuser=False,
                        is_active=True,
                        is_staff=True,
                        email='test@gmail.com',
                        date_joined=date.today())
        new_user.save()
        new_user.set_password(request.POST['password'])
        new_user.save()

        new_employee_user = EmployeeUser(user_id=new_user.id,
                                         employee_id=request.POST['name'],
                                         isActive=True,
                                         insertUser=request.user.id,
                                         insertDate=date.today(),
                                         project='1')
        new_employee_user.save()

        new_user_group_obj = UserGroupTable(group_id_id=group_id,
                                            user_id=new_employee_user,
                                            isActive=True,
                                            insertUser=request.user.id,
                                            insertDate=date.today(),
                                            project='1')
        new_user_group_obj.save()
        context['message'] = 'New user created successfully!!'

    assigned_user = EmployeeUser.objects.all().values('employee_id')

    employee_list = Employee.objects.exclude(employee_id__in=assigned_user).order_by('employeeName')
    user_group = GroupTable.objects.filter(isActive=True)
    user_list = UserGroupTable.objects.filter(isActive = True)

    #print(employee_list)
    context['employee_list'] = employee_list
    context['user_group'] = user_group
    context['active_user_list'] = user_list

    paginator = Paginator(user_list, 100)
    page = request.GET.get('page')

    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)

    context['contacts'] = contacts

    if request.is_ajax():
        data = {}
        username = request.POST.get('username')
        if User.objects.filter(username=username).exists():
            json_message = "Username is already taken"
            data['json_message'] = json_message
            return JsonResponse(data)




    return render(request, 'account/employee_user.html', context)

@login_required
def add_new_menu(request):

    context = {}
    menu_list = MenuTable.objects.filter(isActive=True)
    group_list = GroupTable.objects.filter(isActive=True)
    menu_group_list = MenuGroupTable.objects.filter(isActive=True)
    message = ''


    if request.method == 'POST':
        menu_title = request.POST['menu_title']
        menu_url = request.POST['url_link']
        selected_groups = request.POST.getlist('groups')
        print('values are')
        #print(selected_groups)
        parent_id = ''

        if 'parent_check' not in request.POST:
            parent_id = int(request.POST['parent_name'])
            parent_menu_obj = get_object_or_404(MenuTable, pk=parent_id)

            new_menu_obj, created = MenuTable.objects.get_or_create(
                menu_string = menu_title,
                url_string = menu_url,
                parent_id = parent_menu_obj,
                defaults= {
                    'group_permission_id' : '1',
                    'isActive' : True,
                    'insertUser' : request.user.id,
                    'insertDate' : date.today(),
                    'project' : '1',
                    'has_child' : False,
                }
            )

            if created:

                for list in selected_groups:
                    menu_group_obj = MenuGroupTable(menu_group_id_id=list,
                                                menu_id=new_menu_obj,
                                                insertDate=date.today(),
                                                insertUser=request.user.id,
                                                isActive=True,
                                                project='1')

                    menu_group_obj.save()

                parent_menu_obj.has_child = True
                parent_menu_obj.url_string = '#'
                parent_menu_obj.save()

            else:
                message = 'Menu is already created & added'

        else:
            new_menu_obj, created = MenuTable.objects.get_or_create(
                menu_string = menu_title,
                url_string = menu_url,
                defaults= {
                    'group_permission_id' : '1',
                    'isActive' : True,
                    'insertUser' : request.user.id,
                    'insertDate' : date.today(),
                    'project' : '1',
                    'has_child' : False,
                }
            )

            if created:
                for list in selected_groups:
                    menu_group_obj = MenuGroupTable(menu_group_id_id=list,
                                                    menu_id=new_menu_obj,
                                                    insertDate=date.today(),
                                                    insertUser=request.user.id,
                                                    isActive=True,
                                                    project='1')

                    menu_group_obj.save()

                message = "New Menu has been created"

            else:
                message = 'Menu is already created & added'

    context['menu_list'] = menu_list
    context['message'] = message
    context['active_group_list'] = group_list
    context['menu_group_list'] = menu_group_list

    return render(request, 'account/add_menu.html', context)


@login_required
def add_user_group(request):

    context = {}

    if request.method == 'POST':
        group_name = request.POST['group_name']

        new_group_obj, created = GroupTable.objects.get_or_create(
            group_name = group_name,
            defaults= {
                'isActive' : True,
                'insertUser' : request.user.id,
                'insertDate' : date.today(),
                'project' : '1',

            }
        )

        if created:
            message = 'New user group is created'

        else:
            message = 'User group as same name already exists'

        context['message'] = message

    group_list = GroupTable.objects.filter(isActive=True)
    user_list = UserGroupTable.objects.filter(isActive = True)

    context['active_group_list'] = group_list
    context['active_user_list'] = user_list

    return render(request, 'account/add_user_group.html', context)

@login_required
def user_calender(request):

    if request.is_ajax():
        data = []

        holiday_list = YearlyHoliday.objects.filter(isActive=True, year=date.today().year)


        flag = holiday_list[0].flag
        title = holiday_list[0].holidayTitle
        start = holiday_list[0].date

        for list in holiday_list:
            if list.flag == flag:
                end = list.date + timedelta(days=1)

            elif list.flag != flag:
                data.append({'title' : title, 'start' : start, 'end' : end})
                flag = list.flag
                title = list.holidayTitle
                start = list.date
                end = list.date
        data.append({'title' : title, 'start' : start, 'end' : end})
        data.append({'title' : title, 'start' : '2017-03-24', 'end' : '2017-03-28'})


        # data = [
        #     {
        #         'title': 'event1',
        #         'start': '2017-03-01'
        #     },
        #     {
        #         'title': 'event2',
        #         'start': '2017-03-05',
        #         'end': '2010-01-07'
        #     }
        # ]
        print(data)
        return JsonResponse(data, safe=False)

    return render(request, 'account/user_calender.html')