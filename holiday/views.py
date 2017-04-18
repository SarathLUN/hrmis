from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import WeekDays, WeeklyHoliday, YearlyHoliday
from django.template import loader
from django.core.urlresolvers import reverse
from datetime import date, datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from HRM.myScript import convert_to_date
from django.http import JsonResponse
from hr.models import Location

@login_required
def addWeeklyHoliday(request):
    context = {}
    obj = WeekDays.objects.all()
    location_list = Location.objects.filter(isActive=True)

    context['days'] = obj

    context['location_list'] = location_list

    weekend_list = WeeklyHoliday.objects.filter(isActive=True)
    context['weekend_list'] = weekend_list

    return render(request, 'holiday/addWeeklyHoliday.html', context)


@login_required
def addWeeklyHolidayPerfomed(request):

    value = request.POST.getlist('dayName')
    new_startDate = convert_to_date(request.POST['date'])
    old_endDate = new_startDate - timedelta(days=1)
    location = request.POST.getlist('location')
    print(location)


    weekday = WeekDays.objects.filter(status = True)
    for q in weekday:
        q.status = False
        q.save()

    for list in location:

        query_set = WeeklyHoliday.objects.filter(isActive = True, active_location_id = list)
        for q in query_set:
            q.isActive = False
            q.effectiveEnd = old_endDate
            q.updateUser = request.user.id
            q.updateDate = date.today()
            q.save()

        for val in value:
            day = WeekDays.objects.get(dayNum=val)
            day.status = True
            day.save()
            obj = WeeklyHoliday(dayNum = day.dayNum,
                                effectiveFrom = new_startDate,
                                effectiveEnd = datetime.max.date(),
                                dayName = day.dayname,
                                active_location_id = list,
                                isActive = True,
                                insertUser = request.user.id,
                                insertDate = date.today())
            obj.save()

    return HttpResponseRedirect(reverse('holiday:addWeeklyHoliday'))


@login_required
def addYearlyHoliday(request):
    context = {}

    if request.is_ajax():
        data = {}
        holiday_name = request.POST.get('holiday_name')

        if YearlyHoliday.objects.filter(holidayTitle=holiday_name, year=date.today().year).exists():
            data['ajax_message'] = False
            data['ajax_text'] = 'Holiday as same name already exist for current year!!'
        else:
            data['ajax_message'] = True

        return JsonResponse(data)

    try:
        first_holiday = YearlyHoliday.objects.filter(year=date.today().year, isActive=True).order_by('date')[0]
        flagCount = first_holiday.flag
        fromDate = first_holiday.date
        title = first_holiday.holidayTitle

        holiday_list = YearlyHoliday.objects.filter(year=date.today().year, isActive=True).order_by('date')
        keys = ['holidayTitle', 'fromDate', 'toDate', 'flag']
        #flagCount = holiday_list[0].flag
        #title = holiday_list[0].holidayTitle
        #fromDate = holiday_list[0].date
        edit_list = []
        for obj in holiday_list:
            if obj.flag == flagCount:
                toDate = obj.date

            elif obj.flag != flagCount:
                edit_list.append({'flag': flagCount, 'holidayTitle': title, 'toDate': toDate, 'fromDate': fromDate, })
                flagCount = obj.flag
                title = obj.holidayTitle
                fromDate = obj.date
                toDate = obj.date
        edit_list.append({'flag': flagCount, 'holidayTitle': title, 'toDate': toDate, 'fromDate': fromDate})
        #print(edit_list)
        context = {'holiday_list' : holiday_list,
                   'edit_list' : edit_list}
    except IndexError:
        context['error_message'] = 'No List'

    return render(request, 'holiday/addYearlyHoliday.html', context)


@login_required
def addYearlyHolidayPerfomed(request):
    startDate = convert_to_date(request.POST['start_date'])
    endDate = convert_to_date(request.POST['end_date'])

    dayCount = abs(endDate-startDate).days + 1
    try:
        flagCount = YearlyHoliday.objects.latest('id').id + 1

    except ObjectDoesNotExist:
        flagCount = 1

    for days in range(0,dayCount):

        obj = YearlyHoliday(holidayTitle = request.POST['name'], date = startDate, year = startDate.strftime("%Y"), description = request.POST['comments'], isActive = True, flag = flagCount)
        obj.save()

        startDate = startDate + timedelta(days=1)
        #print(startDate.strftime("%Y"))

    return HttpResponseRedirect(reverse('holiday:addYearlyHoliday'))


@login_required
def editYearlyHolidayPerfomed(request,flag_id):

    get_days = YearlyHoliday.objects.filter(flag=flag_id).delete()


    startDate = convert_to_date(request.POST['start_date'])
    endDate = convert_to_date(request.POST['end_date'])

    dayCount = abs(endDate-startDate).days + 1
    try:
        flagCount = YearlyHoliday.objects.latest('id').id + 1

    except ObjectDoesNotExist:
        flagCount = 1

    for days in range(0,dayCount):
        obj = YearlyHoliday(holidayTitle = request.POST['name'], date = startDate, year = startDate.strftime("%Y"), description = request.POST['comments'], isActive = True, flag = flagCount)
        obj.save()
        startDate = startDate + timedelta(days=1)
        print(startDate.strftime("%Y"))

    return HttpResponseRedirect(reverse('holiday:addYearlyHoliday'))

