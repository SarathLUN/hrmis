/**
 * Created by Tusfiqur on 10/20/2015.
 */

$(function () {
        $("#emp_list_print_btn").click(function () {

            var contents = $("#dvContents").html();
            var frame1 = $('<iframe />');
            frame1[0].name = "frame1";
           // frame1.css({ "position": "relative", "top": "-1000000px" });
            $("body").append(frame1);
            var frameDoc = frame1[0].contentWindow ? frame1[0].contentWindow : frame1[0].contentDocument.document ? frame1[0].contentDocument.document : frame1[0].contentDocument;
            frameDoc.document.open();
            //Create a new HTML document.

            frameDoc.document.write('<html><head><title>Attendance History</title>');
            frameDoc.document.write('<meta http-equiv="X-UA-Compatible" content="IE=edge" />');
            frameDoc.document.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />');

            frameDoc.document.write('<meta name="viewport" content="width=device-width, initial-scale=1" />');

            //Append the external CSS file.
            frameDoc.document.write('<link href="/static/attendance/css/theme-default.css" rel="stylesheet" type="text/css" media="print" />');
            frameDoc.document.write('</head><body>');

            //Append the DIV contents.
            frameDoc.document.write('<div style="font-size: 10px;">');
            frameDoc.document.write(contents);
            frameDoc.document.write('</div>');
            frameDoc.document.write('</body></html>');
            frameDoc.document.close();
            setTimeout(function () {
                window.frames["frame1"].focus();
                window.frames["frame1"].print();
                frame1.remove();
            }, 500);
        });
    });

$("#assigned_employee").hide();

    $("#custom_add_btn_id").hide();


    $(".my_row").click(function(){

        $("#unassigned_employee").hide();
        $("#assigned_employee").show();

        var name = $(this).attr("id");
        var emp_des_id = name.substring(3);

        var emp_id = $("#"+name).find(".b").text();
        var dept_id = $("#"+name).find(".c").text();
        var des_id = $("#"+name).find(".d").text();
        var loc_id = $("#"+name).find(".e").text();
        var startDate_id = $("#"+name).find(".f").text();
        var supervisor_id = $("#"+name).find(".g").text();
        var isActive_id = $("#"+name).find(".h").text();
        var status_id = $("#"+name).find(".i").text();
        var form_action = "/hr/" + emp_des_id + "/editEmployeeDesignation_admin/";

        var emp_id_hidden = $("#hidden_"+name).val();
        $("#hidden_emp_id").val(emp_id_hidden);



        $("#btn_save").text("update");
        $("#custom_add_btn_id").show();

      /*  $("#id_employeeId option:selected").removeAttr("selected");
        $('#id_employeeId option:contains("' + emp_id + '")').filter(function(index){
            return $(this).text() === emp_id;
        }).prop("selected", "selected");
        $("#id_employeeId").change();
        $('#id_employeeId option:not(:selected)').prop('disabled', true);

        */

        $("#id_employeeName").val(emp_id);


        $("#id_departmentId option:selected").removeAttr("selected");
        $('#id_departmentId option:contains("' + dept_id + '")').filter(function(index){
            return $(this).text() === dept_id;
        }).prop("selected", 'selected');
        $("#id_departmentId").change();

        $("#id_designationId option:selected").removeAttr("selected");
        $('#id_designationId option:contains("' + des_id + '")').filter(function(index){
            return $(this).text() === des_id;
        }).prop("selected", "selected");
        $("#id_designationId").change();

        $("#id_location option:selected").removeAttr("selected");
        $('#id_location option:contains("' + loc_id + '")').filter(function(index){
            return $(this).text() === loc_id;
        }).prop("selected", "selected");
        $("#id_location").change();

        $("#id_supervisor option:selected").removeAttr("selected");
        $('#id_supervisor option:contains("' + supervisor_id + '")').filter(function(index){
            return $(this).text() === supervisor_id;
        }).prop("selected", "selected");
        $("#id_supervisor").change();

        $("#id_status option:selected").removeAttr("selected");
        $('#id_status option:contains("' + status_id + '")').filter(function(index){
            return $(this).text() === status_id;
        }).prop("selected", "selected");
        $("#id_status").change();

        $("#id_isActive option:selected").removeAttr("selected");
        $('#id_isActive option:contains("' + isActive_id + '")').filter(function(index){
            return $(this).text() === isActive_id;
        }).prop("selected", "selected");
        $("#id_isActive").change();

        $("#id_startDate").val(startDate_id);

        $(".form-horizontal").attr('action', form_action);


    });

    $("#custom_add_btn_id").click(function () {

        var form_action = "/hr/addEmployeeDesignationPerfomed/";

        $("#assigned_employee").hide();
        $("#unassigned_employee").show();


        $("#id_employeeId option:selected").removeAttr("selected");
        $('#id_employeeId option:contains("Select")').filter(function(index){
            return $(this).text() === "Select";
        }).prop("selected", "selected");
        $("#id_employeeId").change();
        $('#id_employeeId option:not(:selected)').prop('disabled', true);

       $("#id_departmentId option:selected").removeAttr("selected");
        $('#id_departmentId option:contains("Select")').filter(function(index){
            return $(this).text() === "Select";
        }).prop("selected", 'selected');
        $("#id_departmentId").change();


       // $('#id_departmentId').children('option:not(:first)').remove();
       // $("#id_departmentId").append('<option value="option6">option6</option>');

        $("#id_designationId option:selected").removeAttr("selected");
        $('#id_designationId option:contains("Select")').filter(function(index){
            return $(this).text() === "Select";
        }).prop("selected", "selected");
        $("#id_designationId").change();

        $("#id_location option:selected").removeAttr("selected");
        $('#id_location option:contains("Select")').filter(function(index){
            return $(this).text() === "Select";
        }).prop("selected", "selected");
        $("#id_location").change();

        $("#id_supervisor option:selected").removeAttr("selected");
        $('#id_supervisor option:contains("Select")').filter(function(index){
            return $(this).text() === "Select";
        }).prop("selected", "selected");
        $("#id_supervisor").change();

        $("#id_startDate").val('');

        $(".form-horizontal").attr('action', form_action);

        $(this).hide();

    });


