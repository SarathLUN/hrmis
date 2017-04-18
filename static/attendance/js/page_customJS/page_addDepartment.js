/**
 * Created by Tusfiqur on 11/19/2015.
 */



    $("#id_dept_form").submit(function(event){
        if($("#id_departmentName").val() === ''){
            $( "#custom_name_span_id" ).text( "Department name cannot be empty!!" ).show().fadeOut( 3000 );
            event.preventDefault();
        }

    });

    $("#custom_add_btn_id").hide();
    $("#custom_message_id").fadeOut(7000);

    $(".my_row").click(function(){
        var name = $(this).attr("id");

        var dept_name = $("#"+name).find(".b").text();
        var dept_location = $("#"+name).find(".c").text();
        var dept_id = name.substring(3);
        var form_action = "/hr/" + dept_id + "/departmentEdit/";
        //alert(dept_id);
        $("#id_location").val(dept_location);
        $("#id_departmentName").val(dept_name);
        $(".form-horizontal").attr('action', form_action);
        $("#btn_save").text("update");
        $("#custom_panel_heading_id").text("Edit Current Department");
        $("#custom_add_btn_id").show();
    });

    $("#custom_add_btn_id").click(function(){
        var form_action = "/hr/addDepartmentPerfomed/";
       // alert(form_action);
        $("#id_location").val('');
        $("#id_departmentName").val('');
        $(".form-horizontal").attr('action', form_action);
        $("#btn_save").text("Add New");
        $("#custom_panel_heading_id").text("Add New Department");
        $("#custom_add_btn_id").hide();
    });
