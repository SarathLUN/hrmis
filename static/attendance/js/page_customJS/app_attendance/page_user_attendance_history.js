/**
 * Created by Tusfiqur on 3/20/2016.
 */

 $('#id_attendance_search_form input:checkbox').change(function(){

        if($(this).is(':checked')){

            $("#id_child_emp_id").prop('required', false);
            $("#id_child_emp_id").validate();
            $("#id_child_emp_id").hide();

        }
        else{
            $("#id_child_emp_id").prop('required', true);
            $("#id_child_emp_id").show();
        }

    });


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