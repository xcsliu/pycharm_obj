'''
ak	    是	无	用户的访问密钥。只支持浏览器端AK和Android/IOS SDK的AK，服务端AK不支持sn校验方式。
mcode	否	无	安全码。若为Android/IOS SDK的ak, 该参数必需。
width	否	400	图片宽度，范围[10,1024]
height	否	300	图片高度，范围[10,512]
location	是	无	全景位置点坐标。坐标格式：lng<经度>，lat<纬度>，例如116.313393,40.047783。
coordtype	否	bd09ll	全景位置点的坐标类型，目前支持bd09ll（百度坐标），wgs84ll（GPS坐标）和gcj02（google，高德，soso坐标）。
poiid	是	无	poi的id，该属性通常通过place api接口获取，poiid与panoid、location一起设置全景的显示场景，优先级为：poiid>panoid>location。其中根据poiid获取的全景视角最佳。
panoid	是	无	全景图id，panoid与poiid、location一起设置全景的显示场景，优先级为：poiid>panoid>location。
heading	否	0	水平视角，范围[0,360]
pitch	否	0	垂直视角，范围[0,90]。
fov	    否	90	水平方向范围，范围[10,360]，fov=360即可显示整幅全景图

'''

street_view_url_pattern = '  http://source.map.baidu.com/panorama/v2?ak={}&width=512&height=256&location={},{}&fov=180'
