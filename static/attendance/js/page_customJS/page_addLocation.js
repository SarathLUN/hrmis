/**
 * Created by Tusfiqur on 10/19/2015.
 */


    $("#id_dept_form").submit(function(event){
        if($("#id_locationName").val() === ''){
            $( "#custom_name_span_id" ).text( "Location name cannot be empty!!" ).show().fadeOut( 3000 );
            event.preventDefault();
        }

    });
    $("#custom_add_btn_id").hide();
    $("#custom_message_id").fadeOut(7000);

    $(".my_row").click(function () {
        var name = $(this).attr("id");

        var loc_id = name.substring(3);
        var loc_name = $("#" + name).find(".b").text();
        var loc_code = $("#" + name).find(".c").text();
        var loc_des = $("#" + name).find(".d").text();
        var form_action = "/hr/" + loc_id + "/locationEdit/";
         //alert(loc_id);
        $("#id_locationName").val(loc_name);
        $("#id_locationCode").val(loc_code);
        $("#id_description").val(loc_des);
        $(".form-horizontal").attr('action', form_action);
        $("#btn_save").text("update");
        $("#custom_panel_heading_id").text("Edit Location");
        $("#custom_add_btn_id").show();
    });

    $("#custom_add_btn_id").click(function(){
        var form_action = "/hr/addLocationPerfomed/";
       // alert(form_action);
        $("#id_locationName").val('');
        $("#id_locationCode").val('');
        $("#id_description").val('');
        $(".form-horizontal").attr('action', form_action);
        $("#btn_save").text("Add New");
        $("#custom_panel_heading_id").text("Add New Location");
        $("#custom_add_btn_id").hide();
    });
