/*
Js para hacer el combo Unidad dependiente del combo Administrado
*/

$('#id_administrado').change(function(){

  $.get("seguimiento/obtener_unidades/" + $('#id_administrado').val() + "/",
    function (data){
      $('#id_unidad').html(data);
    }
, "html")
});


$('#id_tipo_supervision').change(function(){

  $.get("seguimiento/obtener_subtipos_supervision/" + $('#id_tipo_supervision').val() + "/",
    function (data){
      $('#id_sub_tipo_supervision').html(data);
    }
, "html")
});


