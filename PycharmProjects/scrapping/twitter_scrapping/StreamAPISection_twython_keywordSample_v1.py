'''
The purpose of this code is to demonstrate how to use twython to connection to Twitter's streaming API and download tweets containing certain keywords.

The script has been tested on Mac OS X 10.11.3 (El Capitan) and Python 3.5.

NB: For examples of the tweepy library, see the following tutorials:
	- http://socialmedia-class.org/twittertutorial.html
	- https://pythonprogramming.net/twitter-api-streaming-tweets-python-tutorial/
	- http://adilmoujahid.com/posts/2014/07/twitter-analytics/
	- http://badhessian.org/2012/10/collecting-real-time-twitter-data-with-the-streaming-api/
'''

# Import libraries
import twython as twy
import json
import datetime as dt

# Key, secret, token, token_secret for one of my developer accounts.
# Update with your own strings as necessary
APP_KEY = 'z5JSjzaSSBOD7L6s4oRjbiWmC'
APP_SECRET = 'FTIxEDX7fLUOPzPCT3ntd2t2L2QIKgIEsstNSTqVoAwaVjZbAL'
OAUTH_TOKEN = '1348855934-IkHdBwiLkhcyFoxHY65Nk8J66BqoGC1bdQabxnO'
OAUTH_TOKEN_SECRET = '7FWRIksqVP4xFN5XfxygtAndXpUceCdKSvHERhY2S3iCl'

# Make class
class MyStreamer(twy.TwythonStreamer):
    fileDirectory = '/home/francois/Documents/twitter_scrapping/'  # Any result from this class will save to this directory
    stop_time = dt.datetime.now() + dt.timedelta(minutes=10)  # Connect to Twitter for x minutes.  Comment out if do not want it timed.
    
    def on_success(self, data):
        print(self)
        if dt.datetime.now() > self.stop_time:  # Once minutes=60 have passed, stop.  Comment out these 2 lines if do not want timed connection.
            raise Exception('Time expired')
        test =json.dumps(data, ensure_ascii=False)
        json_load = json.loads(test)
        # séléction du texte des tweets
        compteur_hashtags = 0


        try:
            print(json_load['quoted_status'], ['extended_tweet'], ['full_text'])
        except KeyError:
            print("pas de quoted status")
        try:
            # boucle for qui cherche dans la structure json du tweet pour trouver les hashtags contenant aquarius
            for i in range(len(json_load['retweeted_status']['extended_tweet']['entities']['hashtags'])):
                if json_load['retweeted_status']['extended_tweet']['entities']['hashtags'][i]['text'] == "Aquarius":
                    compteur_hashtags = compteur_hashtags + 1
            print(json_load['retweeted_status']['extended_tweet']['entities']['hashtags'])
            print(json_load['retweeted_status']['extended_tweet']['full_text'])
        except KeyError:
            try:
                for i in range(len(json_load['extended_tweet']['entities']['hashtags'])):
                    if json_load['extended_tweet']['entities']['hashtags'][i]['text'] == "Aquarius":
                        compteur_hashtags = compteur_hashtags + 1
                print(json_load['extended_tweet']['entities']['hashtags'])
                print(json_load['extended_tweet']['full_text'])

            except KeyError:
                for i in range(len(json_load['entities']['hashtags'])):
                    if json_load['entities']['hashtags'][i]['text'] == "Aquarius":
                        compteur_hashtags = compteur_hashtags + 1
                print(json_load['entities']['hashtags'])
                print(json_load['text'])


        #print("nombre de hashtags aquarius :" + str(compteur_hashtags))
        fileName = self.fileDirectory + 'Tweets_' + dt.datetime.now().strftime("%Y_%m_%d_%H") + '.json'  # File name includes date out to hour.
        open(fileName, 'a').write(json.dumps(data, ensure_ascii=False) + '\n')  # Append tweet to the file
    # NB: Because the file name includes the hour, a new file is created automatically every hour.

    def on_error(self, status_code, data):
        fileName = self.fileDirectory + dt.datetime.now().strftime("%Y_%m_%d_%H") + '_Errors.txt'
        open(fileName, 'a').write(json.dumps(data) + '\n')


# Make function.  Tracks key words.
def streamConnect(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET):
    stream = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    stream.statuses.filter(track=['mer bateau françois'], language=['fr'])


# Execute
streamConnect(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
