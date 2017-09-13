b = '''
<!DOCTYPE html>
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
	<style type="text/css">
		body, html {{width: 100%; height: 100%; margin: 0; font-family:"";}}
		#allmap{{width: 100%; height: 100%;}}
		p{{margin-left: 5px; font-size: 14px;}}
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
	map.centerAndZoom(new BMap.Point({}), {});
	  
	map.disable3DBuilding();
	
	var styleJson = [
        {{
            "featureType": "poi",
            "elementType": "all",
            "stylers": {{
                "visibility": "off"
            }}
        }},
        {{
            "featureType": "building",
            "elementType": "all",
            "stylers": {{
                "color": "#000000"
            }}
        }},
        {{
            "featureType": "local",
            "elementType": "labels",
            "stylers": {{
                "visibility": "off"
            }}
        }},
        {{
            "featureType": "subway",
            "elementType": "all",
            "stylers": {{
                "visibility": "off"
            }}
        }},
        {{
            "featureType": "arterial",
            "elementType": "labels",
            "stylers": {{
                "visibility": "off"
            }}
        }},
        {{
            "featureType": "manmade",
            "elementType": "all",
            "stylers": {{
                "visibility": "off"
            }}
        }},
        {{
            "featureType": "label",
            "elementType": "all",
            "stylers": {{
                "visibility": "off"
            }}
        }}
    ]
	map.setMapStyle({{styleJson:styleJson}});
    
    var polyline = new BMap.Polyline([{}], {{strokeColor:"blue", strokeWeight:2, strokeOpacity:1}});  //创建多边形
	map.addOverlay(polyline);   //增加多边形
</script>

'''




import pandas as pd
import json
from shapely.geometry import Polygon



city_name = 'beijing'
# ===========================
community_border_file_path = 'E:\\x-kool-home\\community_and_building\\{}_community_border_with_bd09_2017_09_14.tsv'.format(city_name)


community_border_data = pd.read_table(community_border_file_path, error_bad_lines=False)

community_border_list = []
for idx,row in community_border_data.iterrows():
    community_border = json.loads(community_border_data.bd09[idx])
    # community_border_list.append(community_border)

    point_pattern = 'new BMap.Point({:.9}, {:.9})'
    coordinate_list = []
    for coordinate in community_border:
        point = point_pattern.format(coordinate[0],coordinate[1])
        coordinate_list.append(point)
    ploygon_str = ', '.join(coordinate_list)
    
    community_polygon_obj = Polygon(community_border)
    center_lng = list(community_polygon_obj.centroid.coords)[0][0]
    center_lat = list(community_polygon_obj.centroid.coords)[0][1]
    center_coordinate = '{:.9}, {:.9}'.format(center_lng, center_lat)
    
    zoom = 18
    
    
    html = b.format(center_coordinate, zoom, ploygon_str)
    
    with open('E:\\playground\\script\\{}\\{}_community_{}.html'.format(city_name, city_name, str(idx)), 'a') as f:
        f.write(html)



'''
community_border = community_border_list[6]
# =====================================
point_pattern = 'new BMap.Point({:.9}, {:.9})'
coordinate_list = []
for coordinate in community_border:
    point = point_pattern.format(coordinate[0],coordinate[1])
    coordinate_list.append(point)
ploygon_str = ', '.join(coordinate_list)

community_polygon_obj = Polygon(community_border)
center_lng = list(community_polygon_obj.centroid.coords)[0][0]
center_lat = list(community_polygon_obj.centroid.coords)[0][1]
center_coordinate = '{:.9}, {:.9}'.format(center_lng, center_lat)

zoom = 18


html = b.format(center_coordinate, zoom, ploygon_str)

with open('test_to_build_with_py_{}.html'.format(str(idx)), 'a') as f:
    f.write(html)

'''
