import requests
import time
import json

infile_name= '/home/francois/Documents/base_tweets_train.json'


def get_text_and_post(json_load, nom):
        data = {"nom": "%s" % nom, "structureJSON": "%s" % json_load}
        r = requests.post("https://mds-dev.sinay.fr/api/tweet", data=data)
        print(r.status_code, r.reason)
        if r.status_code == 429:
            print("en attente de pouvoir renvoyer des requêtes au serveur")
            time.sleep(70)
            r = requests.post("https://mds-dev.sinay.fr/api/tweet", data=data)
            print(r.status_code, r.reason)

with open(infile_name, 'r') as infile:
    raw_text = infile.read()
    json_load_all = json.loads(raw_text)
    for i in range(len(json_load_all)):
        json_load = json_load_all[i]['structureJSON']
        nom  = json_load_all[i]['nom']
        get_text_and_post(json_load, nom)
