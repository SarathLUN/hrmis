/**
 * Created by Tusfiqur on 7/27/2016.
 */

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
    $("#id_type").change(function(e) {

        //Prevent default submit. Must for Ajax post.Beginner's pit.



        //Prepare csrf token
        var csrftoken = getCookie('csrftoken');

        //Collect data from fields
        var type = $(this).val();


        //This is the Ajax post.Observe carefully. It is nothing but details of where_to_post,what_to_post
        //Send data
        $.ajax({
            url : window.location.href, // the endpoint,commonly same url
            type : "POST", // http method
            async : false,
            data : { csrfmiddlewaretoken : csrftoken,
                     type_val : type
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