from datetime import datetime
import json
import re

date_re = re.compile("\d+/\d+/\d+ \d+[APM]+", re.M)

def get_date_strs(str):
  return date_re.findall(str)

def reformat(data):
  final=[]
  for row in data:
    for i in range(0,int(row.get("Metric"))):
      #print(row)
      latlng = list(map(float,row.get("Value").split(",")))
      latlng.reverse()
      final.append({
    	  "type": "Feature",
        "id": "%s %s" % (row.get("Value"), get_date_strs(row.get("TooltipHtml"))[i]),
    	  "geometry": {
    	    "type": "Point",
    	    "coordinates": latlng
    	  },
    	  "properties": {
    	    "date_str": get_date_strs(row.get("TooltipHtml"))[i],
          "date": datetime.strptime(get_date_strs(row.get("TooltipHtml"))[i], "%m/%d/%y %I%p").isoformat()
    	  }
    	})
  return final

with open("data/nypd_shooting_incidents_ytd.json") as f:
  data = json.loads(f.read())

with open("data/nypd_shooting_incidents_ytd.geojson", "w") as f2:
  f2.write(json.dumps({
    "type": "FeatureCollection",
    "features": reformat(data)
  }))

with open("data/nypd_murders_ytd.json") as f:
  data = json.loads(f.read())

with open("data/nypd_murders_ytd.geojson", "w") as f2:
  f2.write(json.dumps({
    "type": "FeatureCollection",
    "features": reformat(data)
  }))