/**
 * Created by Tusfiqur on 11/5/2015.
 */

    var flag = 1;
    $("#form_div").hide();

    $("#btn_save").click(function(){

            form_action = "/holiday/addWeeklyHolidayPerfomed/";
            $(".form-horizontal").attr('action', form_action);

    });
    $("#btn_edit").click(function(){
        $("#form_div").show();

    });
