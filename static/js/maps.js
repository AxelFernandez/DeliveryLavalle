let rectangle;
let map;
let infoWindow;

function initMap() {

    map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: -32.758236, lng: -68.402477 },
        zoom: 16
    });
    var limits = document.getElementById("id_limits").value
    if (limits != ""){
        var json = JSON.parse(limits)
        var northJson = json.north;
        var southJson = json.south;
        var eastJson = json.east;
        var westJson = json.west;
    }else{
        var northJson = -32.754954;
        var southJson = -32.758975;
        var eastJson = -68.399872;
        var westJson =  -68.404060;

    }
    const bounds = {
        north: northJson,
        south: southJson,
        west: westJson,
        east: eastJson
    };
  // Define the rectangle and set its editable property to true.
    rectangle = new google.maps.Rectangle({
        bounds: bounds,
        editable: true,
        draggable: true
    });
    rectangle.setMap(map);
    // Add an event listener on the rectangle.
    rectangle.addListener("bounds_changed", showNewRect);
    // Define an info window on the map.
    infoWindow = new google.maps.InfoWindow();
}

function showNewRect() {

    const ne = rectangle.getBounds().getNorthEast();
    const sw = rectangle.getBounds().getSouthWest();
    const contentString =
        '{"north": ' + ne.lat().toFixed(6) + ',' +
        '"east": ' + ne.lng().toFixed(6) + ',' +
        '"south": ' + sw.lat().toFixed(6) + ',' +
        '"west": ' + sw.lng().toFixed(6) + '}';
    return contentString;
}

    $(document).ready(function() {
        $("#cont").hide()
        $("#id_limits").hide()
        $("#id_photo").attr('accept', 'image/x-png,image/jpeg');
        $("#fade").click(function(){
             $("#map").fadeOut("slow");
             $("#map_message").fadeOut("slow");
             $("#map_panel").fadeOut("slow");
             $("#fade").fadeOut("slow");
             $("#cont").fadeIn("slow")
             document.getElementById("id_limits").value = showNewRect();

        })
    });


    function getLimitsAsString(all_overlays){
        var result = "["
        for (var i = 0 ; i < all_overlays.length ; i++) {
            var lat = all_overlays[i][0]
            var long = all_overlays[i][1]
            result += "["+ long + "," + lat + "]"

            if (i != all_overlays.length-1){
                result += ","
            }
        }
        result += "]"
        return result

    }

function checkSize() {

    var preview = document.querySelector('img');
    var file    = document.querySelector('input[type=file]').files[0];
    var reader  = new FileReader();

    if (file) {
        var FileSize = file.size / 1024 / 1024; // in MB
        if (FileSize > 1) {
            $("#warning-image").show()
        }
    }
}

