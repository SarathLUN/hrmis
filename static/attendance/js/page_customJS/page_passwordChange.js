/**
 * Created by Tusfiqur on 12/9/2015.
 */

   $("#btn_save").submit(function(event){
       if($("#id_new_password_re").val() != $("#id_new_password")){
           alert(5);
           event.preventDefault();
       }
   });
