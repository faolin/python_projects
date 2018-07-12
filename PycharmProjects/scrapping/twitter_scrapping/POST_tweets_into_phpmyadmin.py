import twython as twy
import json
import datetime as dt
import requests
import time
''' Se connecte a twitter APi streaming, récupére en temps réel des tweets contenant les mots clés précisés et les envoie a une base phpmyadmin'''


# Key, secret, token, token_secret for one of my developer accounts.
# Update with your own strings as necessary
APP_KEY = 'z5JSjzaSSBOD7L6s4oRjbiWmC'
APP_SECRET = 'FTIxEDX7fLUOPzPCT3ntd2t2L2QIKgIEsstNSTqVoAwaVjZbAL'
OAUTH_TOKEN = '1348855934-IkHdBwiLkhcyFoxHY65Nk8J66BqoGC1bdQabxnO'
OAUTH_TOKEN_SECRET = '7FWRIksqVP4xFN5XfxygtAndXpUceCdKSvHERhY2S3iCl'


class MyStreamer(twy.TwythonStreamer):
    stop_time = dt.datetime.now() + dt.timedelta(minutes=60)  # Connect to Twitter for x minutes.  Comment out if do not want it timed.

    def on_success(self, data):
        if dt.datetime.now() > self.stop_time:  # Once minutes=10 have passed, stop.  Comment out these 2 lines if do not want timed connection.
            raise Exception('Time expired')
        data_dump = json.dumps(data, ensure_ascii=False)
        json_load = json.loads(data_dump)
        # séléction du texte des tweets

        def get_text_and_post(data_dump, json_load, structurejson1 , sctructurejson2 , structurejson3):
            if structurejson3 != None:
                tweet_quoted_texte = json_load[structurejson1][sctructurejson2][structurejson3]
                # print(tweet_quoted_texte)
                data = {"nom": "%s" % tweet_quoted_texte, "structureJSON": "%s" % data_dump}
                r = requests.post("https://mds-dev.sinay.fr/api/tweet", data=data)
                print(r.status_code, r.reason)
                if r.status_code == 429:
                    print("en attente de pouvoir renvoyer des requêtes au serveur")
                    time.sleep(70)
                    r = requests.post("https://mds-dev.sinay.fr/api/tweet", data=data)
                    print(r.status_code, r.reason)

            if structurejson3 == None and sctructurejson2 != None:
                tweet_quoted_texte = json_load[structurejson1][sctructurejson2]
                # print(tweet_quoted_texte)
                data = {"nom": "%s" % tweet_quoted_texte, "structureJSON": "%s" % data_dump}
                r = requests.post("https://mds-dev.sinay.fr/api/tweet", data=data)
                print(r.status_code, r.reason)
                if r.status_code == 429:
                    print("en attente de pouvoir renvoyer des requêtes au serveur")
                    time.sleep(70)
                    r = requests.post("https://mds-dev.sinay.fr/api/tweet", data=data)
                    print(r.status_code, r.reason)

            if structurejson3 == None and sctructurejson2 == None:
                tweet_quoted_texte = json_load[structurejson1]
                # print(tweet_quoted_texte)
                data = {"nom": "%s" % tweet_quoted_texte, "structureJSON": "%s" % data_dump}
                r = requests.post("https://mds-dev.sinay.fr/api/tweet", data=data)
                print(r.status_code, r.reason)
                if r.status_code == 429:
                    print("en attente de pouvoir renvoyer des requêtes au serveur")
                    time.sleep(70)
                    r = requests.post("https://mds-dev.sinay.fr/api/tweet", data=data)
                    print(r.status_code, r.reason)

        try:
            get_text_and_post(data_dump, json_load, 'quoted_status', 'extended_tweet', 'full_text')
        except KeyError:
            print("pas de quoted status")
        try:
            get_text_and_post(data_dump, json_load, 'retweeted_status', 'extended_tweet', 'full_text')
        except KeyError:
            try:
                get_text_and_post(data_dump, json_load, 'extended_tweet', 'full_text', None)
            except KeyError:
                get_text_and_post(data_dump, json_load, 'text', None, None)

    def on_error(self, status_code, data):
        print(status_code, data)

# Make function.  Tracks key words.
def streamConnect(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET):
    stream = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    stream.statuses.filter(track=['Fiber Cable Link', 'subsea', 'submarine cable', 'sea cable','submarine networks', 'Singapore Cable', 'Singapore subsea cable', 'offshore manager', 'ASC', 'SACS', 'Angola Cables', 'undersea', 'deep sea', 'Fibre networks', 'subsea routes', 'superconducting cables', 'broadband investment', 'Southern Cross cable', 'submarine cable system', 'submarine power cables', 'Submarine Systems', 'wind cable', 'Offshore Wind', 'Fiber Cable', 'geotechnical', 'safnog', 'geophysical', 'geochemical', 'offshorewind', 'marine life', 'pollute beach', 'Ocean Conservation', 'pollute sea', 'pollute ocean' 'marine activities', 'endangered species', 'Marine Conservation Zones', 'protected ocean', 'underwater world', 'marine environment', 'Cable System', 'maritime sectors', 'Submarine Telecoms', 'offshore renewables industry', 'wind turbines', 'wind energy', 'offshore environment', 'offshore pipes', 'Offshore Renewable Energy', 'Offshore Services', 'store offshore', 'offshore energy', 'offshore gas', 'offshore oil', 'offshore platform' 'fishing industry', 'Sustainable fisheries', 'marine protection'], language=['fr', 'en'])


# Execute
streamConnect(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
