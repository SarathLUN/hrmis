/**
 * Created by Tusfiqur on 10/12/2015.
 */
$(".my_row").click(function(){
    var name = $(this).attr("id");

    var dept_name = $("#"+name).find(".b").text();
    var dept_location = $("#"+name).find(".c").text();
    var dept_id = $("#"+name).find(".a").text();
    var form_action = "/hr/" + dept_id + "/departmentEdit/";
   // alert(form_action);
    $("#id_location").attr("value", dept_location);
    $("#id_departmentName").attr("value", dept_name);
    $(".form-horizontal").attr('action', form_action);
    $("#btn_save").text("update");
});