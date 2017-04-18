/**
 * Created by Tusfiqur on 11/26/2015.
 */

    $("#id_name").prop('disabled', true);
    $("#id_amount").prop('disabled', true);
    $("#id_startDate").prop('disabled', true);
    $("#id_endDate").prop('disabled', true);
    $("#id_description").prop('disabled', true);
    $("#select_div").hide();
    $("#approved_by_select_div").hide();
   // $('#id_gender').prop('disabled', 'disabled');


    $("input[type=radio]").on("click", function(){
        if($("input[type=radio]:checked").val() == 'edit'){
            $("#id_name").prop('disabled', false);
            $("#id_amount").prop('disabled', false);
            $("#id_startDate").prop('disabled', true);
            $("#id_endDate").prop('disabled', true);
            $("#id_description").prop('disabled', false);
            $('#id_gender').prop('disabled', false);
            $("#input_div").hide();
            $("#select_div").show();
            $("#approved_by_input_div").hide();
            $("#approved_by_select_div").show();

        }
        else if($("input[type=radio]:checked").val() == 'inactivate'){
            $("#id_name").prop('disabled', true);
            $("#id_amount").prop('disabled', true);
            $("#id_startDate").prop('disabled', true);
            $("#id_endDate").prop('disabled', false);
            $("#id_description").prop('disabled', true);
            $("#select_div").hide();
            $("#input_div").show();
            $("#approved_by_input_div").show();
            $("#approved_by_select_div").hide();

        }
        else if($("input[type=radio]:checked").val() == 'modify'){
            $("#id_name").prop('disabled', true);
            $("#id_amount").prop('disabled', false);
            $("#id_startDate").prop('disabled', false);
            $("#id_endDate").prop('disabled', true);
            $("#id_description").prop('disabled', false);

        }

    });
