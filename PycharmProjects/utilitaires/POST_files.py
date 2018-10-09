'''envoie un fichier a un webservice toutes les 30s'''

import requests
import time

def sendFilesAgain():
    with open('report.xls', 'rb') as f:
        r = requests.post('http://httpbin.org/post', files={'/home/francois/Documents/FiletoUpload.json': f})
    time.sleep(30)
    sendFilesAgain()
sendFilesAgain()