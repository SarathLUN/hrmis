/**
 * Created by Tusfiqur on 10/19/2015.
 */
    $("#id_dept_form").submit(function(event){
        if($("#id_designationName").val() === ''){
            $( "#custom_name_span_id" ).text( "Department name cannot be empty!!" ).show().fadeOut( 3000 );
            event.preventDefault();
        }

    });
    $("#custom_add_btn_id").hide();
    $("#custom_message_id").fadeOut(7000);

    $(".my_row").click(function(){
        var name = $(this).attr("id");

        var des_name = $("#"+name).find(".b").text();
        var des_code = $("#"+name).find(".c").text();
        var des_id = name.substring(3);
        var form_action = "/hr/" + des_id + "/designationEdit/";
        //alert(des_id);
        $("#id_designationName").val(des_name);
        $("#id_designationCode").val(des_code);
        $("#id_dept_form").attr('action', form_action);
        $("#btn_save").text("update");
        $("#custom_panel_heading_id").text("Edit Current Department");
        $("#custom_add_btn_id").show();

    });

    $("#custom_add_btn_id").click(function(){
        var form_action = "/hr/addDesignationPerfomed/";
       // alert(form_action);
        $("#id_designationName").val('');
        $("#id_designationCode").val('');
        $(".form-horizontal").attr('action', form_action);
        $("#btn_save").text("Add New");
        $("#custom_panel_heading_id").text("Add New Designation");
        $("#custom_add_btn_id").hide();
    });