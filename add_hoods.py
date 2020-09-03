import shapely
import json
from shapely.geometry import shape
from shapely.strtree import STRtree

def toshape(s):
	a = shape(s['geometry'])
	a.properties = s['properties']
	return a

with open("data/nypd_shooting_incidents_ytd.geojson") as f:
	point_data = json.loads(f.read())

with open("geo/Borough Boundaries.geojson") as f:
	borough_data = STRtree([toshape(x) for x in json.loads(f.read())['features']])

with open("geo/nyc_hoods_filtered.geojson") as f:
	hood_data = STRtree([toshape(x) for x in json.loads(f.read())['features']])

with open("geo/Police Precincts.geojson") as f:
	precinct_data = STRtree([toshape(x) for x in json.loads(f.read())['features']])

with open("geo/brooklyn_roads.geojson") as f:
	street_data = STRtree([toshape(x) for x in json.loads(f.read())['features']])

for idx, point in enumerate(point_data["features"]):
	pt = shape(point["geometry"])
	for borough in borough_data.query(pt):
		if borough.contains(pt):
			point_data['features'][idx]['properties']['borough'] =  borough.properties['boro_name']
			break
	for hood in hood_data.query(pt):
		if hood.intersects(pt):
			point_data['features'][idx]['properties']['neighborhood'] =  hood.properties['Name']
			break
	for precinct in precinct_data.query(pt):
		if precinct.intersects(pt):
			point_data['features'][idx]['properties']['precinct'] =  precinct.properties['precinct']
			break
	close_streets = [s for s in street_data.query(pt) if s.intersects(pt.buffer(0.00015)) and s.properties['FULLNAME']]
	close_streets.sort(key=lambda x: pt.distance(x))
	point_data['features'][idx]['properties']['streets'] =  [s.properties['FULLNAME'] for s in close_streets[:2]]

with open("processed/compstat_with_hoods.geojson", "w") as f:
	f.write(json.dumps(point_data))


with open("data/NYPD Shooting Incident Data (Year To Date).geojson") as f:
	point_data = json.loads(f.read())

for idx, point in enumerate(point_data["features"]):
	pt = shape(point["geometry"])
	for hood in hood_data.query(pt):
		if hood.intersects(pt):
			point_data['features'][idx]['properties']['neighborhood'] =  hood.properties['Name']
			break
	close_streets = [s for s in street_data.query(pt) if s.intersects(pt.buffer(0.00015)) and s.properties['FULLNAME']]
	close_streets.sort(key=lambda x: pt.distance(x))
	point_data['features'][idx]['properties']['streets'] =  [s.properties['FULLNAME'] for s in close_streets[:1]]


with open("processed/quarterly_with_hoods.geojson", "w") as f:
	f.write(json.dumps(point_data))


