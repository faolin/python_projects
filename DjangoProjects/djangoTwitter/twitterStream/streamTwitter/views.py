from django.shortcuts import render
from django.http import HttpResponse
from twython import TwythonStreamer

#clé secrétes twitter
APP_KEY = '****'
APP_SECRET= '***'
OAUTH_TOKEN = '******'
OAUTH_TOKEN_SECRET = '*****'

class MyStreamer(TwythonStreamer):
    def on_stop(self):
        self.disconnect()
    def on_success(self, data):
        if 'text' in data:
            print(data['text'])
    def on_error(self, status_code, data):
        print(status_code)
        
#on initalise le stream
stream = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


#démarage du stream
def startStream(request):
    stream.statuses.filter(track='paris')
    return HttpResponse('stream cut')

#stop the stream   
def stopStream(request):
    MyStreamer.on_stop(stream)
    return HttpResponse('stream coupé')

