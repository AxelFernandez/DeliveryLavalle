
$(document).ready(function() {
    $("#cont").hide()

$("#fade").click(function(){
     $("#map").fadeOut("slow");
     $("#map_message").fadeOut("slow");
     $("#map_panel").fadeOut("slow");
     $("#fade").fadeOut("slow");
     $("#cont").fadeIn("slow")
})
});

