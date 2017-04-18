/**
 * Created by Tusfiqur on 11/5/2015.
 */

    var form_check = true;

    $("#custom_add_btn_id").hide();

    $(".my_row").click(function(){
        var name = $(this).attr("id");

        var flag = name.slice(3);

        var title = $("#"+name).find(".b").text();
        var startDate = $("#"+name).find(".c").text();
        var endDate = $("#"+name).find(".d").text();
        var form_action = "/holiday/" + flag + "/editYearlyHolidayPerfomed/";

        $("#id_name").val(title);
        $("#id_startDate").val( startDate);
        $("#id_endDate").val(endDate);
        //$("#id_ref").attr("value", flag);
        $(".form-horizontal").attr('action', form_action);
        $("#btn_save").html("update <span class='fa fa-refresh fa-right'></span>");

        $("#custom_add_btn_id").show();
        form_check = false;

        var validator = $( "#id_dept_form" ).validate();
        validator.resetForm();

    });

    $("#custom_add_btn_id").click(function(){



        $("#id_name").val('');
        $("#id_startDate").val('');
        $("#id_endDate").val('');
        //$("#id_ref").attr("value", flag);
        $(".form-horizontal").attr('action', "/holiday/addYearlyHolidayPerfomed/");
        $("#btn_save").html("Save <span class='fa fa-floppy-o fa-right'></span>");
        $("#custom_add_btn_id").hide();

        form_check = true;
    });






    //For getting CSRF token
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    //For doing AJAX post
    //When submit is clicked
    $("#id_dept_form").submit(function(e) {

        //Prevent default submit. Must for Ajax post.Beginner's pit.



        //Prepare csrf token
        var csrftoken = getCookie('csrftoken');

        //Collect data from fields
        var holiday_name = $("#id_name").val();


        //This is the Ajax post.Observe carefully. It is nothing but details of where_to_post,what_to_post
        //Send data
        $.ajax({
            url : window.location.href, // the endpoint,commonly same url
            type : "POST", // http method
            async : false,
            data : { csrfmiddlewaretoken : csrftoken,
                     holiday_name : holiday_name
                    }, // data sent with the post request

            // handle a successful response
            success : function(json) {
                console.log(json); // another sanity check
                //On success show the data posted to server as a message
                //alert('Hi   '+json['emp_list'][0].e_name);
                // $('#select2').append('<option value="foo" selected="selected">Foo</option>');


                if(json['ajax_message']==false && form_check==true){

                    $("#custom_message_id").text(json['ajax_text']);
                    e.preventDefault();
                    $("#custom_message_id").fadeOut(8000);
                }

                // var selectedOption = 'green';

                //select.val(selectedOption);
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                console.log(xhr.status + ": " + xhr.responseText);
               // provide a bit more info about the error to the console
            }
        });
    });