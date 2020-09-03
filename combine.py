import json


with open("processed/quarterly_with_hoods.geojson") as f:
	quarterly = json.loads(f.read())

with open("processed/compstat_with_hoods.geojson") as f:
	compstat = json.loads(f.read())

with open("data/nypd_murders_ytd.geojson") as f:
	murders = json.loads(f.read())
	murder_ids = [m.get('id') for m in murders.get('features')]

def quarterly_dt(dts,ts):
	date = dts.split('T')[0]
	return date + 'T' + ts[:-3]

def clean_race(race):
	if race == 'BLACK':
		return 'Black'
	elif race == 'BLACK HISPANIC':
		return 'Black hispanic'
	return race.lower()

final=[]
for pt in quarterly.get('features'):
	props = pt.get('properties')
	final.append({
  	  "type": "Feature",
  	  "geometry": pt.get('geometry'),
  	  "properties": dict(
		incident_key=props.get('incident_key'),
		quarterly=True,
		precinct=props.get('precinct'),
		hood=props.get('neighborhood'),
		boro=props.get('boro').title(),
		vic_sex=props.get('vic_sex') if props.get('vic_sex') != 'U' else None,
		vic_age_group=props.get('vic_age_group'),
		vic_race=clean_race(props.get('vic_race')),
		datetime=quarterly_dt(props.get('occur_date'),props.get('occur_time')),
		date=props.get('occur_date').split('T')[0],
		homicide=props.get('statistical_murder_flag') == 'true',
		homicide_str=props.get('statistical_murder_flag'),
		streets=props.get('streets'),
		link='',
		link_text=''
		)
  	  }
	)

for pt in filter(lambda x: x['properties']['date'] >= '2020-07-01', compstat.get('features')):
	props = pt.get('properties')
	final.append({
  	  "type": "Feature",
  	  "geometry": pt.get('geometry'),
  	  "properties": dict(
		incident_key=pt.get('id'),
		quarterly=False,
		precinct=props.get('precinct'),
		hood=props.get('neighborhood'),
		boro=props.get('borough').title(),
		vic_sex=None,
		vic_age_group=None,
		vic_race=None,
		datetime=props.get('date')[:16],
		date=props.get('date').split('T')[0],
		homicide=pt.get('id') in murder_ids,
		homicide_str="true" if pt.get('id') in murder_ids else "false",
		streets=props.get('streets'),
		link='',
		link_text=''
		)
  	  }
	)

final.sort(key=lambda x: x['properties']['datetime'], reverse=True)
final = list(filter(lambda x: x['properties']['boro'] == 'Brooklyn', final))
with open("templates/js/shootings_combined.geojson", "w") as f2:
  f2.write(json.dumps({
    "type": "FeatureCollection",
    "features": final
  }))
