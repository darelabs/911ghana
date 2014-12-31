


index = """

	<html>


		<head>
		<!-- <meta name="viewport" content="initial-scale=1.0, user-scalable=no" /> -->
		<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
		<script type="text/javascript">
		  function initialize() {
			var latlng = new google.maps.LatLng(5.571908,-0.207367);
			var myOptions = {
			  zoom: 13,
			  center: latlng,
			  mapTypeId: google.maps.MapTypeId.ROADMAP
			};
			var map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);

/*
			var marker = new google.maps.Marker({
				  position: new google.maps.LatLng(5.571908,-0.207367), 
				  map: map,
				  title:"Hello World!"
			  });
*/
			
			var georssLayer = new google.maps.KmlLayer("http://siteopen911.appspot.com/rsscrime");
			georssLayer.setMap(map);
		  }
			

			
		</script>
		</head>


		<body onload="initialize()">
		
		<table width=100%% height=100%% >
			<tr>
				<td width=5%% valign=top>
					%(msg)s &nbsp;
				</td>
				<td>
					<div id="map_canvas" style="width:100%%; height:100%%"></div>			
				</td>
			</tr>
		</table>

		</body>
	</html>

"""



officer_loc = """

	<html>

		<body>
			%(msg)s <p />
			<form name="call-log" method="post">
				Officer <br>
				<input name="officer" type="text"><br />
				Last known location<br />
				<input name="last_known_location" type="text"><br />
				<input name="update-loc" type="submit" value="update loc"><br />
		</body>
	</html>


"""
