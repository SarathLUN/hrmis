/**
 * Created by Tusfiqur on 2/28/2016.
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
 $("#id_department").change(function(e) {

//Prevent default submit. Must for Ajax post.Beginner's pit.
 e.preventDefault();

//Prepare csrf token
 var csrftoken = getCookie('csrftoken');


//Collect data from fields

 var department = $('#id_department option:selected').val();

//This is the Ajax post.Observe carefully. It is nothing but details of where_to_post,what_to_post
//Send data
 $.ajax({
       url : window.location.href, // the endpoint,commonly same url
       type : "POST", // http method
       data : { csrfmiddlewaretoken : csrftoken,
       department : department
 }, // data sent with the post request

 // handle a successful response
 success : function(json) {
 console.log(json); // another sanity check
 //On success show the data posted to server as a message
 //alert('Hi   '+json['emp_list'][0].e_name);
// $('#select2').append('<option value="foo" selected="selected">Foo</option>');
        var newOptions = {
            'red' : 'Red',
            'blue' : 'Blue',
            'green' : 'Green',
            'yellow' : 'Yellow'
        };
       // var selectedOption = 'green';
        var select = $('#id_employee');
        if(select.prop) {
          var options = select.prop('options');
        }
        else {
          var options = select.attr('options');
        }
        $('option', select).remove();

        $.each(json['emp_list'], function(val, text) {
            options[options.length] = new Option(json['emp_list'][val].e_name, json['emp_list'][val].e_id);
        });
        //select.val(selectedOption);
 },

 // handle a non-successful response
 error : function(xhr,errmsg,err) {
 console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
 }
 });
});