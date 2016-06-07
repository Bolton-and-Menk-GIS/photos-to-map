# photos-to-map
Takes a folder location of geotagged photos and creates a simple web map to display them.  This requires Python to be installed.  To use, simply double click on the PhotoMapperUI.pyw which should launch the following GUI:

![Photo Mapper Tool](https://github.com/CalebM1987/CalebM1987.github.io/blob/master/images/photo_gui.PNG)

This gives you two options:

1. Create a new portable app. This will copy all the photos to a new directory (as specified by the output folder) as well as the HTML page and "bin" folder containing OSM plugin and points.js file.  This is useful for sharing the app.

2. Embed in original photo directory.  This will just make the HTML page in the same location where the photos reside.  This option is much faster and does not require the photos to be copied anywhere else.  A "bin" folder will be created that has the OSM plugin and the points.js file.

When the tool is complete, it will launch the HTML page which is a map.  This uses the Google Maps API and the [Overlapping Marker Spiderfier](https://github.com/jawj/OverlappingMarkerSpiderfier) plugin to handle overlapping markers.  The map will look something like this:

![Web Map](https://github.com/CalebM1987/CalebM1987.github.io/blob/master/images/photomap_example.PNG)
