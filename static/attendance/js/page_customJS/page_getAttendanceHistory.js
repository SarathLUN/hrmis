/**
 * Created by Tusfiqur on 12/21/2015.
 */

    $("#printBtn").click(function () {
        var contents = $("#dvContents").html();
        var frame1 = $('<iframe />');
        frame1[0].name = "frame1";
       // frame1.css({ "position": "relative", "top": "-1000000px" });
        $("body").append(frame1);
        var frameDoc = frame1[0].contentWindow ? frame1[0].contentWindow : frame1[0].contentDocument.document ? frame1[0].contentDocument.document : frame1[0].contentDocument;
        frameDoc.document.open();
        //Create a new HTML document.

        frameDoc.document.write('<html><head><title>Attendance History</title>');
        frameDoc.document.write('<meta http-equiv="X-UA-Compatible" content="IE=edge" />');
        frameDoc.document.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />');

        frameDoc.document.write('<meta name="viewport" content="width=device-width, initial-scale=1" />');

        //Append the external CSS file.
        frameDoc.document.write('<link href="/static/attendance/css/theme-default.css" rel="stylesheet" type="text/css" media="print" />');
        frameDoc.document.write('</head><body>');

        //Append the DIV contents.
        frameDoc.document.write('<div class="col-md-12"> <table> <tr><td style="width: 80%;"></td><td style="width: 20%; text-align: right;"><img src="/static/attendance/img/LamSys-logo-final-inverse_trans.png"  style="height: 40px; width: 140px; text-align: right;"> </td> </tr> </table> </div>');
        frameDoc.document.write('<br><br>');
        frameDoc.document.write(contents);
        frameDoc.document.write('</body></html>');
        frameDoc.document.close();
        setTimeout(function () {
            window.frames["frame1"].focus();
            window.frames["frame1"].print();
            frame1.remove();
        }, 500);
    });


    $("#printBtn2").click(function () {
        var contents = $("#dvContents2").html();
        var frame1 = $('<iframe />');
        frame1[0].name = "frame1";
       // frame1.css({ "position": "relative", "top": "-1000000px" });
        $("body").append(frame1);
        var frameDoc = frame1[0].contentWindow ? frame1[0].contentWindow : frame1[0].contentDocument.document ? frame1[0].contentDocument.document : frame1[0].contentDocument;
        frameDoc.document.open();
        //Create a new HTML document.

        frameDoc.document.write('<html><head><title>Attendance History</title>');
        frameDoc.document.write('<meta http-equiv="X-UA-Compatible" content="IE=edge" />');
        frameDoc.document.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />');

        frameDoc.document.write('<meta name="viewport" content="width=device-width, initial-scale=1" />');

        //Append the external CSS file.
        frameDoc.document.write('<link href="/static/attendance/css/theme-default.css" rel="stylesheet" type="text/css" media="print" />');
        frameDoc.document.write('</head><body>');

        //Append the DIV contents.
        frameDoc.document.write('<div class="col-md-12"> <table> <tr><td style="width: 80%;"></td><td style="width: 20%; text-align: right;"><img src="/static/attendance/img/LamSys-logo-final-inverse_trans.png"  style="height: 40px; width: 140px; text-align: right;"> </td> </tr> </table> </div>');
        frameDoc.document.write('<br><br>');
        frameDoc.document.write(contents);
        frameDoc.document.write('</body></html>');
        frameDoc.document.close();
        setTimeout(function () {
            window.frames["frame1"].focus();
            window.frames["frame1"].print();
            frame1.remove();
        }, 500);
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

                options[options.length] = new Option('Select', '');

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


    $('#id_attendance_search_form input:checkbox').change(function(){
        if($(this).is(':checked')){
            //$("#id_employee").prop("disabled", true);
            var form_action = "/attendance/showAttedanceList/";

        }
        else{
          //  $("#id_employee").prop("disabled", false);
            var form_action = "/attendance/getEmployeeAttendanceHistory/";

        }
        $("#id_attendance_search_form").attr('action', form_action);

    });
/*
$(document).ready(function(){


    $("#id_startDate").datepicker({
        numberOfMonths: 2,
        onSelect: function(selected) {
          $("#id_endDate").datepicker("option","minDate", selected)
        }
    });
    $("#id_endDate").datepicker({
        numberOfMonths: 2,
        onSelect: function(selected) {
           $("#id_startDate").datepicker("option","maxDate", selected)
        }
    });
});
    */