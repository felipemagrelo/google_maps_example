import scraperwiki
import simplejson

# the url is provided by the vienna open data initiative. it returns a json object containing location information (and others) for police stations in vienna.
json = scraperwiki.scrape('http://data.wien.gv.at/daten/wfs?service=WFS&request=GetFeature&version=1.1.0&typeName=ogdwien:POLIZEIOGD&srsName=EPSG:4326&outputFormat=json')

# the json data is loaded into an object. correct file encoding has to be guaranteed, else the json-string can not be parsed and converted into an object
jsonobj = simplejson.loads(json, "ISO-8859-1")

print jsonobj 

# we iterate over all features of the json-object. 1 feature = 1 police station
for geometries in jsonobj['features']:
    # set up our record
    record = {
        'id': None,
        'lat': None,
        'long': None,
        'name': None,
        'address' : None,
    }
    
    # we take the information from each police station, as needed.
    record['id'] = geometries['id']
    record['long'] = geometries['geometry']['coordinates'][0]
    record['lat'] = geometries['geometry']['coordinates'][1]
    record['name'] = geometries['properties']['NAME']
    record['address']= geometries['properties']['ADRESSE']
    
    # we store the record into the datastore...
    scraperwiki.sqlite.save(["id"], record)
