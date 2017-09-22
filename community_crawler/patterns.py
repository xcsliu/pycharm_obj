#!/usr/bin/env python
# coding=utf8

community = """
<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
    <style type="text/css">
        body, html {width: 100%%; height: 100%%; margin: 0; font-family:"";}
        #allmap{width: 100%%; height: 100%%;}
        .anchorBL{display:none}
        p{margin-left: 5px; font-size: 14px;}
    </style>
    <script type="text/javascript" src="http://api.map.baidu.com/api?v=2.0&ak=egdbDG5gl5z2vEGrmGrUSvyDOf77xMGi"></script>
    <title>building map</title>
</head>
<body>
    <div id="allmap"></div>
</body>
</html>
<script type="text/javascript">
    var map = new BMap.Map('allmap');
    map.centerAndZoom(new BMap.Point(%(center)s), 18);
    map.disable3DBuilding();
    
    var styleJson = [
        {"featureType": "building", "elementType": "all", "stylers": {"color": "#FF0000"}},
        {"featureType": "land", "elementType": "all", "stylers": {"color": "#0000FF"}},
        {"featureType": "road", "elementType": "all", "stylers": {"visibility": "off"}},
        {"featureType": "green", "elementType": "all", "stylers": {"visibility": "off"}},
        {"featureType": "water", "elementType": "all", "stylers": {"visibility": "off"}},
        {"featureType": "poi", "elementType": "all", "stylers": {"visibility": "off"}},
        {"featureType": "local", "elementType": "labels", "stylers": {"visibility": "off"}},
        {"featureType": "subway", "elementType": "all", "stylers": {"visibility": "off"}},
        {"featureType": "arterial", "elementType": "labels", "stylers": {"visibility": "off"}},
        {"featureType": "manmade", "elementType": "all", "stylers": {"visibility": "off"}},
        {"featureType": "label", "elementType": "all", "stylers": {"visibility": "off"}}
    ]
    map.setMapStyle({styleJson: styleJson});
    
    surrounding_boundary = [
        %(surrounding_boundary)s
    ]
    map.clearOverlays();
    var polygon = new BMap.Polygon(surrounding_boundary, {strokeWeight: 2, strokeColor: "#FFFFFF", strokeOpacity: 1, fillColor:"#FFFFFF", fillOpacity: 1}); //建立多边形覆盖物
    map.addOverlay(polygon);  //添加覆盖物
</script>
"""
