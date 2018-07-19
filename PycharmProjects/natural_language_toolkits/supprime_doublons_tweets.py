''' supprime les tweets présents plusieurs fois dans notre base'''

import json
input_filenames = '/home/francois/Téléchargements/Base_tweets_atraiter.txt'
outfile_name = '/home/francois/Téléchargements/Base_tweets_sans_doublons.json'
liste_tweets = []
liste_id = []
with open(outfile_name, 'w') as outfile:
    with open(outfile_name, 'r') as infile:
        outfile.write('[')
        raw_text = infile.read()
        json_load = json.loads(raw_text)
        count_doublon = 0
        for i in range(len(json_load)):
            if json_load[i]['nom'] not in liste_tweets:
                liste_tweets.append(json_load[i]['nom'])
                dumped = json.dumps(json_load[i])
                outfile.write(dumped)
                if i != len(json_load)-1:
                    outfile.write(',')
            else:
                print(json_load[i]['nom'])
                count_doublon +=1
        print(len(json_load))
        print(count_doublon)
    outfile.write(']')
