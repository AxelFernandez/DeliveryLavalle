     var drawingManager;
      var all_overlays = [];
      var all_overlays_pure = [];
      var selectedShape;
      var colors = ['#1E90FF'];
      var selectedColor;
      var colorButtons = {};

      function clearSelection() {
        if (selectedShape) {
          selectedShape.setEditable(false);
          selectedShape = null;
        }
      }

      function setSelection(shape) {
        clearSelection();
        selectedShape = shape;
        shape.setEditable(true);
        selectColor(shape.get('fillColor') || shape.get('strokeColor'));
      }

      function deleteSelectedShape() {
        if (selectedShape) {
          selectedShape.setMap(null);
        }
      }

      function deleteAllShape() {
        for (var i=0; i < all_overlays.length; i++)
        {
          all_overlays[i].overlay.setMap(null);
        }

        all_overlays = [];
        all_overlays_pure = [];
        $("#drawing-finished").hide()
        $("#drawing-start-again").show()

      }

      function selectColor(color) {
        selectedColor = color;
        for (var i = 0; i < colors.length; ++i) {
          var currColor = colors[i];
          colorButtons[currColor].style.border = currColor == color ? '2px solid #789' : '2px solid #fff';
        }

        var polygonOptions = drawingManager.get('polygonOptions');
        polygonOptions.fillColor = color;
      }

      function setSelectedShapeColor(color) {
        if (selectedShape) {
          if (selectedShape.type == google.maps.drawing.OverlayType.POLYLINE) {
            selectedShape.set('strokeColor', color);
          } else {
            selectedShape.set('fillColor', color);
          }
        }
      }

      function makeColorButton(color) {
        var button = document.createElement('span');
        button.className = 'color-button';
        button.style.backgroundColor = color;
        google.maps.event.addDomListener(button, 'click', function() {
          selectColor(color);
          setSelectedShapeColor(color);
        });

        return button;
      }

       function buildColorPalette() {
         var colorPalette = document.getElementById('color-palette');
         for (var i = 0; i < colors.length; ++i) {
           var currColor = colors[i];
           var colorButton = makeColorButton(currColor);
           colorPalette.appendChild(colorButton);
           colorButtons[currColor] = colorButton;
         }
         selectColor(colors[0]);
       }

      function initialize() {
        var map = new google.maps.Map(document.getElementById('map'), {
          zoom: 16,
          center: new google.maps.LatLng(-32.758236, -68.402477),
          mapTypeId: google.maps.MapTypeId.ROADMAP,
          disableDefaultUI: true,
          zoomControl: true
        });

        var polyOptions = {
          strokeWeight: 0,
          fillOpacity: 0.45,
          editable: true
        };
        // Creates a drawing manager attached to the map that allows the user to draw
        // markers, lines, and shapes.
        drawingManager = new google.maps.drawing.DrawingManager({
          drawingMode: google.maps.drawing.OverlayType.POLYGON,
          markerOptions: {
            draggable: true
          },
          polylineOptions: {
            editable: true
          },
          rectangleOptions: polyOptions,
          circleOptions: polyOptions,
          polygonOptions: polyOptions,
          map: map
        });

        google.maps.event.addListener(drawingManager, 'overlaycomplete', function(e) {
            all_overlays.push(e);
            });

      google.maps.event.addListener(drawingManager, 'polygoncomplete', function(e) {
           all_overlays_pure.push(e)
           var path = e.getPath()
           var coordinates = [];

           for (var i = 0 ; i < path.length ; i++) {
              var point = []
              point.push(
                path.getAt(i).lat(),
                path.getAt(i).lng()
              );
              coordinates.push(point)
            }
            coordinates.push([path.getAt(0).lat(), path.getAt(0).lng()])
            all_overlays_pure = coordinates;
            $("#fade").show()
            $("#warning-draw").hide()
            $("#drawing-finished").show()

      });


        // Clear the current selection when the drawing mode is changed, or when the
        // map is clicked.
        google.maps.event.addListener(drawingManager, 'drawingmode_changed', clearSelection);
        google.maps.event.addListener(map, 'click', clearSelection);
        google.maps.event.addDomListener(document.getElementById('delete-button'), 'click', deleteSelectedShape);
        google.maps.event.addDomListener(document.getElementById('delete-all-button'), 'click', deleteAllShape);

        buildColorPalette();
      google.maps.event.addDomListener(window, 'load', initialize);
      }

    $(document).ready(function() {
        $("#cont").hide()
        $("#id_limits").hide()
        $("#fade").hide()
        $("#drawing-finished").hide()
        $("#drawing-start-again").hide()
        $("#id_photo").attr('accept', 'image/x-png,image/jpeg');





    $("#fade").click(function(){
         $("#map").fadeOut("slow");
         $("#map_message").fadeOut("slow");
         $("#map_panel").fadeOut("slow");
         $("#fade").fadeOut("slow");
         $("#cont").fadeIn("slow")
         var limits = (getLimitsAsString(all_overlays_pure))
         document.getElementById("id_limits").value = limits;

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


