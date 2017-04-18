/**
 * Created by Tusfiqur on 5/22/2016.
 */
$(document).ready(function(){
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


$("#id_parent").change(function(){


    $("#test_1").prop('checked', true);
    var csrftoken = getCookie('csrftoken');
    var parent = $("#id_parent").val();


    $.ajax({
           url : window.location.href, // the endpoint,commonly same url
           type : "POST", // http method
           async : false,
           data : { csrfmiddlewaretoken : csrftoken,
                    parent_id : parent
            }, // data sent with the post request

     // handle a successful response
     success : function(json) {
        //console.log(json); // another sanity check
        //On success show the data posted to server as a message
        //alert('Hi   '+json['emp_list'][0].e_name);
        // $('#select2').append('<option value="foo" selected="selected">Foo</option>');
           // alert(json['total_days']);

         for(var i =0;i < json['ajax_child_list'].length;i++) {

             //var item = json['ajax_child_list'][i];

         }


     },

     // handle a non-successful response
     error : function(xhr,errmsg,err) {

     console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
     }
     });
});
});