from django.shortcuts import render
from hr.models import Department,Employee,Location,EmployeeDesignation,Designation
from django.contrib.auth.decorators import login_required
from django.db import connection,transaction
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
# Create your views here.

@login_required
def update_table_data(request):
    context = {}

    if request.method == "POST":


        table_name = request.POST['table_name']

        sql_string = "select * from " + table_name
        print(sql_string)
        cursor = connection.cursor()
        cursor.execute(sql_string)
        row = cursor.fetchall()

        context['table_name'] = table_name
        context['table_objects'] = row


    return render(request, 'admin_action/admin_data_update_page.html', context)

@login_required
def delete_data(request,data_id, table_name):

    try:
        sql_string = "show keys from " + table_name + " where key_name = 'PRIMARY'"
        #print(sql_string)
        cursor = connection.cursor()
        cursor.execute(sql_string)
        row = cursor.fetchall()
        for obj in row:
            primary_key = obj[4]

        data_sql_string = "delete from " + table_name + " where " + primary_key + "=" + data_id + ";"
        #print(data_sql_string)
        cursor.execute(data_sql_string)
        output = cursor.fetchall()
        print("output is: ")
        print(output)
    except:
        raise Http404

    return HttpResponseRedirect(reverse("admin_action:update_data"))