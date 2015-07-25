<?xml version="1.0" encoding="ISO-8859-1"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

	<xsl:template match="/">
		<html>
			<head>			
				<script type='text/javascript' src='Chart.js'></script>
			</head>
			<body>
				<table border='1'>
					<xsl:for-each select="nodes/node">
						<tr>
							<td>
								Node: <xsl:value-of select="@id"/>
								<canvas height="500" width="700">
									<xsl:attribute name="id">
										<xsl:value-of select="@id" />
									</xsl:attribute>
								</canvas>
								<script> 					
									var canvas_id = <xsl:value-of select="@id"/>;
									var degree_centrality_value = <xsl:value-of select="degree_centrality"/>
									var closeness_centrality_value = <xsl:value-of select="closeness_centrality"/>;
									var betweenness_centrality_value = <xsl:value-of select="betweenness_centrality"/>;
									var dispersion_centrality_value = <xsl:value-of select="dispersion_centrality"/>;
									var dispersion_average_value = <xsl:value-of select="dispersion_average"/>;
									var dispersion_max_value = <xsl:value-of select="dispersion_max"/>;
									var dispersion_min_value = <xsl:value-of select="dispersion_min"/>;
									var barChartData = {
										labels : ["Degree_centrality","Closeness_centrality","Betweenness_centrality","Dispersion_centrality","Dispersion_average","Dispersion_max", "Dispersion_min"],
										datasets : [
											{
												fillColor : "rgba(151,187,205,0.5)",
												strokeColor : "rgba(151,187,205,1)",
												data : [degree_centrality_value,closeness_centrality_value,betweenness_centrality_value,dispersion_centrality_value,dispersion_average_value,dispersion_max_value,dispersion_min_value]
											}
										]
								 
									}
									var myLine = new Chart(document.getElementById(canvas_id).getContext("2d")).Bar(barChartData);
								</script>
							</td>
							<td>
								<table border='1'>
									<tr>
										<th>Node id</th>										
										<td><xsl:value-of select="@id"/></td>
									</tr>
									<tr>
										<th>Degree_centrality</th>
										<td><xsl:value-of select="degree_centrality"/></td>
									</tr>
									<tr>
										<th>Closeness_centrality</th>
										<td><xsl:value-of select="closeness_centrality"/></td>
									</tr>
									<tr>
										<th>Betweenness_centrality</th>
										<td><xsl:value-of select="betweenness_centrality"/></td>
									</tr>
									<tr>
										<th>Dispersion_centrality</th>
										<td><xsl:value-of select="dispersion_centrality"/></td>
									</tr>
									<tr>
										<th>Dispersion_average</th>
										<td><xsl:value-of select="dispersion_average"/></td>
									</tr>
									<tr>
										<th>Dispersion_max</th>
										<td><xsl:value-of select="dispersion_max"/></td>
									</tr>
									<tr>
										<th>Dispersion_min</th>
										<td><xsl:value-of select="dispersion_min"/></td>
									</tr>
								</table>
							</td>
						</tr>
					</xsl:for-each>
				</table>
			</body>
		</html>
	</xsl:template>
</xsl:stylesheet>