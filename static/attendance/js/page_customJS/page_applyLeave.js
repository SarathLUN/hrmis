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
         $("#id_amount").focusout(function(e) {


        //Prevent default submit. Must for Ajax post.Beginner's pit.
         e.preventDefault();

        //Prepare csrf token
         var csrftoken = getCookie('csrftoken');


        //Collect data from fields

         var startDate = $('#id_startDate').val();
         var amount = $('#id_amount').val();


        //This is the Ajax post.Observe carefully. It is nothing but details of where_to_post,what_to_post
        //Send data
         $.ajax({
               url : window.location.href, // the endpoint,commonly same url
               type : "POST", // http method
               data : { csrfmiddlewaretoken : csrftoken,
                    ajax_type : '2',
                    start_date : startDate,
                    total_amount : amount
         }, // data sent with the post request

         // handle a successful response
         success : function(json) {
            console.log(json); // another sanity check
            //On success show the data posted to server as a message
            //alert('Hi   '+json['emp_list'][0].e_name);
            // $('#select2').append('<option value="foo" selected="selected">Foo</option>');
               // alert(json['total_days']);
                $("#id_endDate").prop("value", json['end_date']);
                $("#id_hidden_to_date").prop("value", json['end_date']);

         },

         // handle a non-successful response
         error : function(xhr,errmsg,err) {
         console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
         }
         });
        });

$("#leave_type").change(function(e){

    e.preventDefault();

    var csrftoken = getCookie('csrftoken');

    var leave_type = $(this).val();

    $.ajax({
        url : window.location.href,
        type : "POST",
        data : { csrfmiddlewaretoken : csrftoken,
            'ajax_type' : '1',
            leave_type : leave_type
        },

        success : function(json){
            var msg = json['ajax_message'];
            var supervisor_id = json['supervisor'];
            var description_val = json['ajax_description'];
            $("#span_confirmed_by").html(msg);
            $("#ajax_message").val(supervisor_id);
            $("#span_description").html(description_val);


        },
        error : function(xhr,errmsg,err) {

            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
         }
    });
});

$(function () {
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

        frameDoc.document.write(contents);
        frameDoc.document.write('</body></html>');
        frameDoc.document.close();
        setTimeout(function () {
            window.frames["frame1"].focus();
            window.frames["frame1"].print();
            frame1.remove();
        }, 500);
    });
});



    $(".e").click(function(){
        var leave_id = $(this).attr("id");
        var id_prefix = leave_id.slice(8);
       // alert(id_prefix);

        var date_range = $("#td_1_tr_"+id_prefix).text();
        $("#modal_start_date").text(date_range);

        var count = $("#td_2_tr_"+id_prefix).text();
        $("#modal_days").text(count);

        var category = $("#td_6_tr_"+id_prefix).text();
        $("#modal_category").text(category);

    });