'''Poste du JSON sur un serveur élasticsearch'''
import json
import requests


url = 'http://localhost:9200/twitter/_doc/'
data = {'sender': 'Alice', 'receiver': 'Bob', 'message': 'We did it!'}
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
r = requests.post(url, data=json.dumps(data), headers=headers)
print(r.text)