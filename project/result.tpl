<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
<style type="text/css">
    body, html,#allmap {width: 100%;height: 90%;margin:0;font-family:"微软雅黑";}
</style>
<script type="text/javascript" src="http://api.map.baidu.com/api?v=2.0&ak=6l5K2xmDZK0HrYEaIp6ujXtp"></script>
<script src="http://libs.baidu.com/jquery/1.9.0/jquery.js" type="text/javascript"></script>
<title>Result</title>
</head>
<body onload = "draw_point();">

<div id = "allmap"></div>

<div>
    <form method="post">
	   <input type="submit" value="back"><br>
    </form>
    <h3> Items that meet the requirements
    <table style="width:100%">
    <tr>
        <td>STATION</td>
        <td>STATION_NAME</td> 
        <td>ELEVATION</td>
        <td>LATITUDE</td>
        <td>LONGITUDE</td>
        <td>DATE</td>
        <td>PRCP</td>
        <td>SNWD</td>
        <td>TMAX</td>
        <td>TMIN</td>
    </tr>
    %for item in Items:
    <tr>
        <td> {{item['STATION']}} </td>
        <td> {{item['STATION_NAME']}} </td>
        <td> {{item['ELEVATION']}} </td>
        <td> {{item['LATITUDE']}} </td>
        <td> {{item['LONGITUDE']}} </td>
        <td> {{item['DATE']}} </td>
        <td> {{item['PRCP']}} </td>
        <td> {{item['SNWD']}}</td>
        <td> {{float(item['TMAX'])/10}}</td>
        <td> {{float(item['TMIN'])/10}}</td>
    </tr>
    %end
    </table>
</div>

<script type="text/javascript">
    // Baidu map API
    var map = new BMap.Map("allmap");    // Create map instance
    map.centerAndZoom(new BMap.Point(116.404, 39.915), 5); 
    map.addControl(new BMap.MapTypeControl());
    map.enableScrollWheelZoom(true);
    it = JSON.parse({"Items":Items})

    function draw_point(){
        var $this = $(this);
        $.getJSON("/search2",function(data){
            $.each(data,function(index,temp){
                var point = new BMap.Point(parseFloat(temp['LONGITUDE']),parseFloat(temp['LATITUDE']));
                var marker = new BMap.Marker(point);
                map.addOverlay(marker);
            });
        });
    }

    function draw_points()
    {
        alert(it.Items)
        for(var i = 0; i < Items.length; i++)
        {
            var point = new BMap.Point(Items[i]['LONGITUDE'],Items[i]['LATITUDE']);
            var marker = new BMap.Marker(point);
            map.addOverlay(marker);
        }
        map.centerAndZoom(point,7);
    }
</script>
</body>
</html>
