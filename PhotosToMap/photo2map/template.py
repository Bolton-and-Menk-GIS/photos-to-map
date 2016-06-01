part1 = """<html>

<head>

    <style type="text/css">
        html {
            height: 100%
        }
        
        body {
            height: 100%;
            margin: 0;
            padding: 0
        }
        
        #map_canvas {
            height: 100%
        }
    </style>
    <script type="text/javascript" src="http://maps.googleapis.com/maps/api/js?&sensor=false">
    </script>
    <script type="text/javascript">
        var locations = """

part2 = """

        function initialize() {

            var myOptions = {
                center: new google.maps.LatLng("""

part3 = """),
                zoom: 13,
                mapTypeId: google.maps.MapTypeId.ROADMAP

            };
            var map = new google.maps.Map(document.getElementById("default"),
                myOptions);

            setMarkers(map, locations)

        }

        function setMarkers(map, locations) {

            var marker, i

            for (i = 0; i < locations.length; i++) {

                
                var lat = locations[i].lat
                var lon = locations[i].lon
                var img_title = locations[i].img_title
		var content = locations[i].content

                latlngset = new google.maps.LatLng(lat, lon);

                var marker = new google.maps.Marker({
                    map: map,
                    title: img_title,
                    position: latlngset
                });
                map.setCenter(marker.getPosition())

                var infowindow = new google.maps.InfoWindow()

                google.maps.event.addListener(marker, 'click', (function(marker, content, infowindow) {
                    return function() {
                        infowindow.setContent(content);
                        infowindow.open(map, marker);
                    };
                })(marker, content, infowindow));

            }
        }
    </script>
</head>

<body onload="initialize()">
    <div id="default" style="width:100%; height:100%"></div>
</body>

</html>"""
