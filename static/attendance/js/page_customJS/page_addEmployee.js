/**
 * Created by Tusfiqur on 11/22/2015.
 */


    $("#custom_message_id").fadeOut(7000);

    var link_id = 'link1';

    $("#link2").click(function(event){

        var value = getValidation(link_id);

        if(value==false){
            event.stopPropagation();

        }
        else{
            link_id = 'link2';
            event.default();
        }


    });

    $("#link3").click(function(event){

        var value = getValidation(link_id);

        if(value==false){
            event.stopPropagation();

        }
        else{
            link_id = 'link3';
            event.default();
        }


    });

    $("#link4").click(function(event){

        var value = getValidation(link_id);

        if(value==false){
            event.stopPropagation();


        }
        else{
            link_id = 'link4';
            event.default();
        }


    });

    $("#link1").click(function(event){

        var value = getValidation(link_id);

        if(value==false){
            event.stopPropagation();

        }
        else{
            link_id = 'link1';
            event.default();
        }


    });

    function getValidation(open_tab){

        if (open_tab == 'link1'){
            var val_name = $("#employee_add_form").validate().element("#id_employeeName");
            var val_dob = $("#employee_add_form").validate().element("#date_of_birth");

            if (val_name && val_dob) {
                return true;
            }
            else {
                return false;
            }
        }

        if (open_tab == 'link2'){

            var val_join_date = $("#employee_add_form").validate().element("#id_join_date");
            var val_card_id = $("#employee_add_form").validate().element("#id_card_id");

            if (val_join_date && val_card_id) {
                return true;
            }
            else {
                return false;
            }
        }

        if (open_tab == 'link3'){

            var val_mobile = $("#employee_add_form").validate().element("#id_mobile");

            if (val_mobile) {
                return true;
            }
            else {
                return false;
            }
        }

        if (open_tab == 'link4'){

            var val_start_date = $("#employee_add_form").validate().element("#id_startDate");

            if (val_start_date) {
                return true;
            }
            else {
                return false;
            }
        }
    }