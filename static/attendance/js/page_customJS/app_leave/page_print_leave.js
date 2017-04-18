/**
 * Created by Tusfiqur on 3/31/2016.
 */

    alert(5);

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

