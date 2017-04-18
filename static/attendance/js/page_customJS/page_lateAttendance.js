/**
 * Created by Tusfiqur on 1/3/2016.

*/

    $("#modal_approval_type").hide();
    $(".child_1").hide();
    $(".child_2").hide();
    $(".child_3").hide();
    $(".child_4").hide();

    $(".show_modal").click(function(){

        var row_id = $(this).attr("id");
        var name = $("#tr_"+row_id).find(".a").text();
        var date = $("#tr_"+row_id).find(".b").text();
        var sms = $("#tr_"+row_id).find(".d").text();

        $("#modal_applicant_name").text(name);
        $("#modal_date").text(date);
        $("#modal_sms_text").text(sms);

    });
    
    $("#modal_sms_type").change(function(){
        val = $(this).val();
        if(val == 'late'){
            $("#modal_approval_type").show();
        }
        else{
            $("#modal_approval_type").hide();
        }
    });

    $(".open_link").click(function(){
        var row_id = $(this).attr("id");
       // $(this).css('background-color', 'blue');
        // hide all open link
        var list_id = row_id.slice(10);
       $("#reject_link_"+list_id).toggle();

        // open only link
        $("#child_1_"+row_id).toggle(500);
        $("#child_2_"+row_id).toggle(500);


    });

    $(".reject_link").click(function(){
        var row_id = $(this).attr("id");
       // $(this).css('background-color', 'blue');
        // hide all open link
        var list_id = row_id.slice(12);
       $("#open_link_"+list_id).toggle(500);

        // open only link
        $("#child_3_"+row_id).toggle(500);
        $("#child_4_"+row_id).toggle(500);


    });