/**
 * Created by Tusfiqur on 12/14/2015.
 */


    $('#id_add_exception_form input:checkbox').change(function(){

        if($(this).is(':checked')){
            $("#id_grace_time").prop("disabled", true);

        }
        else{
            $("#id_grace_time").prop("disabled", false);
        }

    });