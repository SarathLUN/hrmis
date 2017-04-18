

    $('#id_parent_check').change(function(){

        if($(this).is(':checked')){
            $(".parent").hide();
        }
        else{
            $(".parent").show();
        }

    });
