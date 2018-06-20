from nltk.stem.snowball import FrenchStemmer
from nltk.stem.snowball import SnowballStemmer
import glob
import json

input_filenames = glob.glob("/home/francois/Documents/twitter_scrapping/*.json")
output_filename = '/home/francois/Documents/tweets_stemmises.txt'

stemmer = FrenchStemmer()
stemmer_english = SnowballStemmer("english")

with open(output_filename, "w") as outfile:
    for infile_name in input_filenames:
        with open(infile_name) as infile:
            # aprés avoir ouvert le fichier on récupére toutes les données en texte
            infile_to_rawtext = infile.read()
            data = infile_to_rawtext.split("\n")
            #on suprrime le dernier index du tableau car dans notre fichier avec tout les tweets l'on rajoute toujours \n aprés chaque tweet donc on a le dernier index de vide
            del data[-1]
            for i in range(len(data)):
            # on utlise la fonction json.loads pour pouvoir ensuite récuperer des éléments précis de la structure du fichier json
                json_load = json.loads(data[i], 'utf-8')
                liste_mots_stem = ""


                if(json_load['lang']== "fr"):
                    # test pour récupérer le texte du tweet, un tweet peut avoir une structure json différente selon son nombre de charactére, il est donc nécessaire
                    # d'avoir toutes les possibilités de l'emplacement du texte du tweet
                    try:
                        #print(json_load['retweeted_status']['extended_tweet']['entities']['hashtags'])
                        print(json_load['retweeted_status']['extended_tweet']['full_text'])
                        text = json_load['retweeted_status']['extended_tweet']['full_text']
                        text = text.replace(",", "")
                        text = text.split(" ")
                        for i in range(len(text)):
                            liste_mots_stem = liste_mots_stem + " " + stemmer.stem(text[i])
                        print(liste_mots_stem)
                        outfile.write(liste_mots_stem)

                    except KeyError:
                        try:
                            #print(json_load['extended_tweet']['entities']['hashtags'])
                            print(json_load['extended_tweet']['full_text'])
                            outfile.write(stemmer.stem(json_load['extended_tweet']['full_text']) + '\n')
                            text = json_load['extended_tweet']['full_text']
                            text = text.replace(",", "")
                            text = text.split(" ")
                            for i in range(len(text)):
                                liste_mots_stem = liste_mots_stem + " " + stemmer.stem(text[i])
                            print(liste_mots_stem)
                            outfile.write(liste_mots_stem)

                        except KeyError:
                            #print(json_load['entities']['hashtags'])
                            print(json_load['text'])
                            text = json_load['text']
                            text = text.replace(",", "")
                            text = text.split(" ")
                            for i in range(len(text)):
                                liste_mots_stem = liste_mots_stem + " " + stemmer.stem(text[i])
                            print(liste_mots_stem)
                            outfile.write(liste_mots_stem)

                if (json_load['lang'] == "en"):
                    # test pour récupérer le texte du tweet, un tweet peut avoir une structure json différente selon son nombre de charactére, il est donc nécessaire
                    # d'avoir toutes les possibilités de l'emplacement du texte du tweet
                    try:
                        # print(json_load['retweeted_status']['extended_tweet']['entities']['hashtags'])
                        print(json_load['retweeted_status']['extended_tweet']['full_text'])
                        text = json_load['retweeted_status']['extended_tweet']['full_text']
                        text = text.replace(",", "")
                        text = text.split(" ")
                        for i in range(len(text)):
                            liste_mots_stem = liste_mots_stem + " " + stemmer_english.stem(text[i])
                        print(liste_mots_stem)
                        outfile.write(liste_mots_stem)

                    except KeyError:
                        try:
                            # print(json_load['extended_tweet']['entities']['hashtags'])
                            print(json_load['extended_tweet']['full_text'])
                            outfile.write(stemmer_english.stem(json_load['extended_tweet']['full_text']) + '\n')
                            text = json_load['extended_tweet']['full_text']
                            text = text.replace(",", "")
                            text = text.split(" ")
                            for i in range(len(text)):
                                liste_mots_stem = liste_mots_stem + " " + stemmer_english.stem(text[i])
                            print(liste_mots_stem)
                            outfile.write(liste_mots_stem)

                        except KeyError:
                            # print(json_load['entities']['hashtags'])
                            print(json_load['text'])
                            text = json_load['text']
                            text = text.replace(",", "")
                            text = text.split(" ")
                            for i in range(len(text)):
                                liste_mots_stem = liste_mots_stem + " " +stemmer_english.stem(text[i])
                            print(liste_mots_stem)
                            outfile.write(liste_mots_stem)

