import json
import urllib.request
contents = urllib.request.urlopen("https://mds-dev.sinay.fr/api/tweet").read()
contents = contents.decode('utf-8')
json_load = json.loads(contents)
structure_json =(json_load[0]['structureJSON'])

json_load = json.loads(structure_json)
print(json_load)
print(json_load['text'])