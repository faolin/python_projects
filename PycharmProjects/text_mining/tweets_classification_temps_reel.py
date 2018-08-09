
''' récupere en temps réel des tweets avec des mots clés, les nettoie , les classifie selon leur catégorie (Cable sous marin, oil&gas ,Energie marine renouvelable, Fishing
 Shipping grâce a un modéle SVM entrainé sur une base annotée manuellement. Affiche les tweets intéréssant appartenenant a une des catégories et les enregistre pour les archiver'''
# Import libraries
import twython as twy
import json
import datetime as dt
from nltk.stem.snowball import FrenchStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import glob
import nltk
import string
import re
import time
from sklearn.metrics import confusion_matrix
import argparse
from sklearn.externals import joblib

# Key, secret, token, token_secret for one of my developer accounts.
# Update with your own strings as necessary
APP_KEY = 'z5JSjzaSSBOD7L6s4oRjbiWmC'
APP_SECRET = 'FTIxEDX7fLUOPzPCT3ntd2t2L2QIKgIEsstNSTqVoAwaVjZbAL'
OAUTH_TOKEN = '1348855934-IkHdBwiLkhcyFoxHY65Nk8J66BqoGC1bdQabxnO'
OAUTH_TOKEN_SECRET = '7FWRIksqVP4xFN5XfxygtAndXpUceCdKSvHERhY2S3iCl'


''' tout les outils de nettoyage'''
nltk.download('stopwords')
nltk.download('punkt')
input_filenames = glob.glob("/home/francois/Documents/twitter_scrapping/*.json")
output_filename = '/home/francois/Documents/tweets_stemmises.txt'
fichier_emoticone = '/home/francois/python_projects/PycharmProjects/natural_language_toolkits/all_emoji.txt'
stemmer = FrenchStemmer()
stemmer_english = SnowballStemmer("english")
stopWords_fr = set(stopwords.words('french'))
stopWords_en = set(stopwords.words('english'))
tokenizer = TweetTokenizer(reduce_len=True, strip_handles=True, preserve_case=False) #tokenizer qui permet de transformer une phrase en une liste de mots

'''tout les outils de classification'''
MODEL_PATH = 'model.pkl'
SOURCE = 'Base_tweets_finale.json' # base d'entrainement du classifier
ENCODING = "ISO-8859-1"
action = '' # si l'on veut entrainer l'outil sur une base mettre 'train', sinon le laisser vide (si un model.plk existe déja)
#



'''Toutes les fonctions utilisées par le classifier SVM'''


def unigram_process(data): #fonction de vectorisation du texte
    from sklearn.feature_extraction.text import CountVectorizer
    vectorizer = CountVectorizer()
    vectorizer = vectorizer.fit(data)
    return vectorizer


def bigram_process(data):
    from sklearn.feature_extraction.text import CountVectorizer
    vectorizer = CountVectorizer(ngram_range=(1, 2))
    vectorizer = vectorizer.fit(data)
    return vectorizer


def tfidf_process(data):
    from sklearn.feature_extraction.text import TfidfTransformer
    transformer = TfidfTransformer()
    transformer = transformer.fit(data)
    return transformer

def retrieve_data(source_name=SOURCE):
    import pandas as pd
    import numpy as np
    import json
    frac = 0.9

    all_tweets = []
    all_notation = []

    with open(source_name, 'r') as infile:
        '''contents = urllib.request.urlopen("https://mds-dev.sinay.fr/api/tweet").read()
        contents = contents.decode('utf-8')
        json_load = json.loads(contents)
        '''
        raw_text = infile.read()
        json_load = json.loads(raw_text, 'utf-8')

        for i in range(len(json_load)):
            if json_load[i]['interessant'] != None:
                if json_load[i]['nom_nettoye'] != None:
                    all_tweets.append(json_load[i]['nom_nettoye'])
                    all_notation.append(json_load[i]['interessant'])

        df = pd.DataFrame({'tweet': all_tweets, 'interessant': all_notation})
        df['split'] = np.random.randn(df.shape[0], 1)
        msk = np.random.rand(len(df)) <= frac
        train = df[msk]
        print(train)

        test = df[~msk]

    return train['tweet'], train['interessant'], test['tweet'], test['interessant']


def train_sgd(Xtrain, Ytrain): # classifier
    from sklearn.linear_model import SGDClassifier
    classifier = SGDClassifier(loss="hinge", penalty="elasticnet", n_iter=20)  # 'hinge' loss = linear Support Vector Machine (SVM)
    print("SGD Fitting")
    classifier.fit(Xtrain, Ytrain)
    return classifier


def accuracy(Ytrain, Ytest):
    assert (len(Ytrain) == len(Ytest))
    num = sum([1 for i, word in enumerate(Ytrain) if Ytest[i] == word])
    n = len(Ytrain)
    return (num * 100) / n


def write_txt(data, name):
    data = ''.join(str(word) for word in data)
    file = open(name, 'w')
    file.write(data)
    file.close()
    pass


def train_and_test(vectorizer, training_function):

    print ("-----------------------TRAINING THE MODEL---------------------------")
    # avec TF-IDF
    '''Xtrain_uni = vectorizer.transform(Xtrain_text)
    uni_tfidf_transformer = tfidf_process(Xtrain_uni)
    Xtrain_tf_uni = uni_tfidf_transformer.transform(Xtrain_uni)
    classifier = training_function(Xtrain_tf_uni, Ytrain)
    Ytrain_uni = classifier.predict(Xtrain_tf_uni)'''

    # sans TF-IDF
    Xtrain_uni = vectorizer.transform(Xtrain_text)
    classifier = training_function(Xtrain_uni, Ytrain)
    Ytrain_uni = classifier.predict(Xtrain_uni)



    print ("Train accuracy: ", accuracy(Ytrain, Ytrain_uni))
    print ("\n")

    print ("-----------------------TESTING THE MODEL -----------------------")
    Xtest_uni = vectorizer.transform(Xtest_text)
    Ytest_uni = classifier.predict(Xtest_uni)
    print ("Test accuracy: ", accuracy(Ytest, Ytest_uni))
    print ("\n")
    return Ytest_uni, classifier

def tweet_classifier(tweet):
    tweet_vector = vectorizer.transform([tweet])
    tweet_prediction = model.predict(tweet_vector)
    return tweet_prediction

def formattage_date(): # récupére la date d'aujourd'hui et la formatte pour elasticsearch
    today_date = dt.datetime.today()
    split = str(today_date).split(' ')
    annee_mois_jour = split[0]
    heure_min_sec = split[1]
    split_heure_min_sec = heure_min_sec.split(':')
    sec = split_heure_min_sec[-1]
    sec = sec.split('.')
    sec = sec[0]
    heure_min_sec = '%s'%split_heure_min_sec[-3] + ':' + '%s'%split_heure_min_sec[-2] +':'+ str(sec)
    date = annee_mois_jour +"T"+ heure_min_sec
    return date

def post_tweet_elasticsearch(tweet, prediction, json_load): #envoie les tweets à elasticsearch
    import requests
    url = 'http://localhost:9200/twitter/tweets/'
    data = {'tweet': '%s'%tweet, 'categorie': '%d'%prediction, 'date': '%s'%formattage_date(), 'source': '%s'%json.dumps(json_load)} #.strftime("%Y_%m_%d_%H") }
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    print(r.text)

#création du model de classification ou utilisation de celui-ci si il existe déja
if action == 'train':
    Xtrain_text, Ytrain, Xtest_text, Ytest = retrieve_data()
    print("========================UNIGRAM + SGD================================")
    start = time.time()
    vectorizer = bigram_process(Xtrain_text) #on choisit la fonction bigram ou unigram
    y_true, classifier=train_and_test(vectorizer, train_sgd)
    #y_true_bigram=train_and_test(bigram_process(Xtrain_text), train_sgd)
    print ("Time taken: ", time.time() - start, " seconds")
    print ("test",Ytest)
    Matrice_confusion=confusion_matrix(Ytest,y_true)
    print("matrice_confusion_unigram",Matrice_confusion)
    #Matrice_confusion_bigram=confusion_matrix(Ytest,y_true_bigram)
    #print("matrice_confusion_bigram",Matrice_confusion_bigram)

    print ("-----------------------SAVING THE MODEL-----------------------------")
    joblib.dump(classifier, MODEL_PATH)
    joblib.dump(vectorizer, 'vectorizer.pkl')
    print("Model saved.")
else:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load('vectorizer.pkl')
    '''test de classification sur une phrase'''
    test_text = "i enjoy this movie"
    test_vector = vectorizer.transform([test_text])
    prediction = model.predict(test_vector)
    print("prediction", prediction)



# connexion a twitter et récuperation des tweets
    class MyStreamer(twy.TwythonStreamer):
        fileDirectory = '/home/francois/Documents/twitter_scrapping/'  # Any result from this class will save to this directory
        stop_time = dt.datetime.now() + dt.timedelta(
            minutes=3000)  # Connect to Twitter for x minutes.  Comment out if do not want it timed.
        liste_tweets_interessants = []
        reset_liste_time = dt.datetime.now() + dt.timedelta(hours=48)
        def on_success(self, data):
            if dt.datetime.now() > self.stop_time:  # Once minutes=60 have passed, stop.  Comment out these 2 lines if do not want timed connection.
                raise Exception('Time expired')
            '''on supprime la liste des tweets intéréssants permettant de ne pas envoyer de doublons toutes les 48h afin de ne pas surcharger la mémoire'''
            if dt.datetime.now() > self.reset_liste_time:
                print("reset de la liste")
                self.liste_tweets_interessants = []
                self.reset_liste_time = self.reset_liste_time + dt.timedelta(hours =48)
                print("reset du chronométre")
            print("liste des tweets intéréssants :", self.liste_tweets_interessants)
            print("chronométre", self.reset_liste_time)
            tweet = json.dumps(data, ensure_ascii=False)
            json_load = json.loads(tweet)
            # séléction du texte des tweets
            compteur_hashtags = 0


            # toutes les fonctions de nettoyage du tweet
            def remove_stopswords(language, texte_tokenize):
                wordsFiltered = []
                if (language == 'fr'):
                    for w in texte_tokenize:
                        if w not in stopWords_fr:
                            wordsFiltered.append(w)
                    print("remove stopwords", wordsFiltered)
                    return wordsFiltered
                if (language == 'en'):
                    for w in texte_tokenize:
                        if w not in stopWords_en:
                            wordsFiltered.append(w)
                    print("remove stopwords", wordsFiltered)
                    return wordsFiltered

            def stemmatisation(language, texte):
                liste_mots_stem = ""
                if (language == 'fr'):
                    for i in range(len(texte)):
                        liste_mots_stem = liste_mots_stem + " " + stemmer.stem(texte[i])
                if (language == 'en'):
                    for i in range(len(texte)):
                        liste_mots_stem = liste_mots_stem + " " + stemmer_english.stem(texte[i])
                print("stemmatisaton: ", liste_mots_stem)
                return liste_mots_stem

            def remove_url(texte):
                resultat = re.sub(r"http\S+", "", texte)
                if resultat == texte:
                    print("pas d'url detéctée")
                    return texte
                else:
                    print("remove url:", resultat)
                    return resultat

            def remove_username_twitter(texte):  # enléve les user mention et les username d'un tweet
                texte_sans_username = ""
                texte_sans_user_mention = ""

                def all_user_mention_path(texte_sans_user_mention, structurejson1, structurejson2, structurejson3,
                                          structurejson4):
                    if structurejson3 == None and structurejson4 == None:
                        nbr_user_mention = len(json_load[structurejson1][structurejson2])
                        struct_user_mention = json_load[structurejson1][structurejson2]
                    if structurejson4 == None and structurejson3 != None:
                        nbr_user_mention = len(json_load[structurejson1][structurejson2][structurejson3])
                        struct_user_mention = json_load[structurejson1][structurejson2][structurejson3]
                    if structurejson1 != None and structurejson2 != None and structurejson3 != None and structurejson4 != None:
                        nbr_user_mention = len(json_load[structurejson1][structurejson2][structurejson3][structurejson4])
                        struct_user_mention = json_load[structurejson1][structurejson2][structurejson3][structurejson4]

                    for i in range(nbr_user_mention):
                        user_mention = "@" + struct_user_mention[i]['screen_name']
                        if texte_sans_user_mention == "":
                            elem2 = [x for x in texte.split()]
                        else:
                            elem2 = [x for x in texte_sans_user_mention.split()]
                        for item in elem2:
                            index = item.lower().find(user_mention.lower())
                            if index != -1:
                                if texte_sans_user_mention == "":
                                    texte_sans_user_mention = texte.replace(item, "")
                                    texte_sans_user_mention = texte_sans_user_mention.replace(item.lower(), "")
                                else:
                                    texte_sans_user_mention = texte_sans_user_mention.replace(item, "")
                                    texte_sans_user_mention = texte_sans_user_mention.replace(item.lower(), "")
                    return texte_sans_user_mention

                try:
                    texte_sans_user_mention = all_user_mention_path(texte_sans_user_mention, 'quoted_status',
                                                                    'extended_tweet', 'entities', 'user_mentions')
                except KeyError:
                    result = "pas de user mention pour la structure json ci-dessus"
                try:
                    texte_sans_user_mention = all_user_mention_path(texte_sans_user_mention, 'quoted_status', 'entities',
                                                                    'user_mentions', None)
                except KeyError:
                    result = "pas de user mention pour la structure json ci-dessus"
                try:
                    texte_sans_user_mention = all_user_mention_path(texte_sans_user_mention, 'extended_tweet', 'entities',
                                                                    'user_mentions', None)
                except KeyError:
                    result = "pas de user mention pour la structure json ci-dessus"
                try:
                    texte_sans_user_mention = all_user_mention_path(texte_sans_user_mention, 'retweeted_status',
                                                                    'extended_tweet', 'entities', 'user_mentions')
                except KeyError:
                    result = "pas de user mention pour la structure json ci-dessus"
                try:
                    texte_sans_user_mention = all_user_mention_path(texte_sans_user_mention, 'retweeted_status', 'entities',
                                                                    'user_mentions', None)
                except KeyError:
                    result = "pas de user mention pour la structure json ci-dessus"
                try:
                    texte_sans_user_mention = all_user_mention_path(texte_sans_user_mention, 'entities', 'user_mentions',
                                                                    None, None)
                except KeyError:
                    result = "pas de user mention pour la structure json ci-dessus"

                def all_username_path(texte_sans_username, texte_sans_user_mention, structurejson1, structurejson2,
                                      structurejson3):
                    if structurejson3 == None and structurejson2 == None:
                        struct_user_mention = json_load[structurejson1]
                    else:
                        struct_user_mention = json_load[structurejson1][structurejson2][structurejson3]
                    user_mention = "@" + struct_user_mention
                    if texte_sans_user_mention == "":
                        elem3 = [x for x in texte.split()]
                    else:
                        elem3 = [x for x in texte_sans_user_mention.split()]
                    for item in elem3:
                        index = item.lower().find(user_mention.lower())
                        if index != -1:
                            if texte_sans_user_mention == "":
                                texte_sans_username = texte.replace(item, "")
                                texte_sans_username = texte_sans_username.replace(item.lower(), "")
                            else:
                                texte_sans_username = texte_sans_user_mention.replace(item, "")
                                texte_sans_username = texte_sans_username.replace(item.lower(), "")
                        else:
                            if texte_sans_user_mention == "":
                                texte_sans_username = texte
                            else:
                                texte_sans_username = texte_sans_user_mention
                    return texte_sans_username

                try:
                    texte_sans_username = all_username_path(texte_sans_username, texte_sans_user_mention,
                                                            'retweeted_status', 'user', 'screen_name')
                    return texte_sans_username
                except KeyError:
                    result = "pas de user mention pour la structure json ci-dessus"
                try:
                    texte_sans_username = all_username_path(texte_sans_username, texte_sans_user_mention,
                                                            'in_reply_to_screen_name', None, None)
                    return texte_sans_username
                except TypeError:
                    if texte_sans_user_mention == "":
                        return texte
                    else:
                        return texte_sans_user_mention

            def remove_hashtags(texte):
                texte_sans_hashtags = ""

                def all_hashtags_path(texte_sans_hashtags, structurejson1, structurejson2, structurejson3, structurejson4):
                    if structurejson3 == None and structurejson4 == None:
                        nbr_hashtages = len(json_load[structurejson1][structurejson2])
                        struct_hashtags = json_load[structurejson1][structurejson2]
                    if structurejson4 == None and structurejson3 != None:
                        nbr_hashtages = len(json_load[structurejson1][structurejson2][structurejson3])
                        struct_hashtags = json_load[structurejson1][structurejson2][structurejson3]
                    if structurejson1 != None and structurejson2 != None and structurejson3 != None and structurejson4 != None:
                        nbr_hashtages = len(json_load[structurejson1][structurejson2][structurejson3][structurejson4])
                        struct_hashtags = json_load[structurejson1][structurejson2][structurejson3][structurejson4]

                    for i in range(nbr_hashtages):
                        hashtags = "#" + struct_hashtags[i]['text']
                        if texte_sans_hashtags == "":
                            elem2 = [x for x in texte.split()]
                        else:
                            elem2 = [x for x in texte_sans_hashtags.split()]
                        for item in elem2:
                            index = item.find(hashtags)
                            if index != -1:
                                if texte_sans_hashtags == "":
                                    texte_sans_hashtags = texte.replace(item, "")
                                else:
                                    texte_sans_hashtags = texte_sans_hashtags.replace(item, "")
                    return texte_sans_hashtags

                try:
                    texte_sans_hashtags = all_hashtags_path(texte_sans_hashtags, 'quoted_status', 'extended_tweet',
                                                            'entities', 'hashtags')
                except KeyError:
                    result = "pas de hashtags pour la structure json ci-dessus"
                try:
                    texte_sans_hashtags = all_hashtags_path(texte_sans_hashtags, 'quoted_status', 'entities', 'hashtags',
                                                            None)
                except KeyError:
                    result = "pas de hashtags pour la structure json ci-dessus"
                try:
                    texte_sans_hashtags = all_hashtags_path(texte_sans_hashtags, 'extended_tweet', 'entities', 'hashtags',
                                                            None)
                except KeyError:
                    result = "pas de hashtags pour la structure json ci-dessus"
                try:
                    texte_sans_hashtags = all_hashtags_path(texte_sans_hashtags, 'retweeted_status', 'extended_tweet',
                                                            'entities', 'hashtags')
                except KeyError:
                    result = "pas de hashtags pour la structure json ci-dessus"
                try:
                    texte_sans_hashtags = all_hashtags_path(texte_sans_hashtags, 'retweeted_status', 'entities', 'hashtags',
                                                            None)
                except KeyError:
                    result = "pas de hashtags pour la structure json ci-dessus"
                try:
                    texte_sans_hashtags = all_hashtags_path(texte_sans_hashtags, 'entities', 'hashtags', None, None)
                except KeyError:
                    result = "pas de hashtags pour la structure json ci-dessus"

                if texte_sans_hashtags == "":
                    return texte
                else:
                    return texte_sans_hashtags

            def remove_emoji(fichier_emoticone, texte):
                pas_emoticon = ""
                compteur_emote = 0
                with open(fichier_emoticone, "r") as fichier_emoticone:
                    fichier_emoticone_to_rawtext = fichier_emoticone.read()
                    all_emoticone = fichier_emoticone_to_rawtext.split("\n")
                    for y in range(len(all_emoticone)):
                        if all_emoticone[y] in texte:
                            compteur_emote += 1
                            if pas_emoticon == "":
                                pas_emoticon = texte.replace(all_emoticone[y], ' ')
                            else:
                                pas_emoticon = pas_emoticon.replace(all_emoticone[y], ' ')
                    if compteur_emote == 0:
                        return texte
                    else:
                        return pas_emoticon

            # pas utile pour le moment
            def remove_symbols(texte):

                nbr_symbol = len(json_load['entities']['symbols'])
                for i in range(nbr_symbol):
                    symbol = json_load['entities']['symbols'][i]
                    texte = texte.replace(symbol, " ")
                #print("symbols remove:", texte)
                return texte

            def remove_punctuation(texte):
                no_punctuation = texte.translate(str.maketrans({a: " " for a in string.punctuation}))
                no_punctuation = no_punctuation.replace('’', ' ')
                no_punctuation = no_punctuation.replace('«', ' ')
                no_punctuation = no_punctuation.replace('»', ' ')
                no_punctuation = no_punctuation.replace('➡', ' ')
                no_punctuation = no_punctuation.replace('•', ' ')
                no_punctuation = no_punctuation.replace('°', ' ')
                no_punctuation = no_punctuation.replace('×', ' ')
                print("remove punctuation: ", no_punctuation)
                return no_punctuation

            def nettoyer_le_texte(language, texte):  # regroupement de toutes les fonctions pour nettoyer le texte
                no_url = remove_url(texte)
                no_emoji = remove_emoji(fichier_emoticone, no_url)
                '''no_hashtags = remove_hashtags(no_emoji)
                if no_hashtags == no_emoji:
                    print("pas de hashtags détécté")
                else:
                    print("remove hashtags : ", no_hashtags)'''
                remove_username = remove_username_twitter(no_emoji)
                if remove_username == no_emoji:
                    print("pas de username détécté.")
                else:
                    print("remove username :", remove_username)
                no_punctuation = remove_punctuation(remove_username)
                texte_tokenize = tokenizer.tokenize(no_punctuation)
                print("tokenisation : ", texte_tokenize)
                words_stopped = remove_stopswords(language, texte_tokenize)
                texte_stemmatiser = stemmatisation(language, words_stopped)
                return texte_stemmatiser

            def get_tweets_nettoye_classifie(lang, structurejson1, structurejson2, structurejson3):

                if (structurejson3 == None and structurejson2 != None):
                    text = json_load[structurejson1][structurejson2]
                    # on nettoie le texte en faisant appel a plusieurs techniques : stopwords, stemmatisation, on enléve les urls, la ponctuation
                    text_nettoyer = nettoyer_le_texte(lang, text)
                    prediction = tweet_classifier(text_nettoyer)
                    print('prédiction :', prediction[0])
                    if int(prediction[0]) != 0:
                        if text_nettoyer not in self.liste_tweets_interessants:
                            self.liste_tweets_interessants.append(text_nettoyer)
                            print("/////tweet: ", json_load[structurejson1][structurejson2])
                            #print("texte nettoyé:", text_nettoyer)
                            print("prediction :", prediction)
                            post_tweet_elasticsearch(text, int(prediction[0]), json_load)
                            return text_nettoyer
                        else:
                            print("tweet intéssants déja vu")
                    else:
                        print("tweet non-intéréssant")
                        print(text)
                        return None
                    #outfile.write(text_nettoyer)
                if (structurejson3 == None and structurejson2 == None):
                    text = json_load[structurejson1]
                    # on nettoie le texte en faisant appel a plusieurs techniques : stopwords, stemmatisation, on enléve les urls, la ponctuation
                    text_nettoyer = nettoyer_le_texte(lang, text)
                    #on récupere la prédiction du classifier
                    prediction = tweet_classifier(text_nettoyer)
                    print('prédiction :', prediction[0])
                    #outfile.write(text_nettoyer)
                    if int(prediction[0]) != 0:
                        if text_nettoyer not in self.liste_tweets_interessants:
                            self.liste_tweets_interessants.append(text_nettoyer)
                            print("/////tweet: ", json_load[structurejson1])
                            #print("texte nettoyé:", text_nettoyer)
                            print("prediction :", prediction)
                            post_tweet_elasticsearch(text, int(prediction[0]), json_load)
                            return text_nettoyer
                        else:
                            print("tweet intéssants déja vu")
                    else:
                        print("tweet non-intéréssant")
                        print(text)
                        return None
                if (structurejson3 != None and structurejson2 != None):
                    text = json_load[structurejson1][structurejson2][structurejson3]
                    # on nettoie le texte en faisant appel a plusieurs techniques : stopwords, stemmatisation, on enléve les urls, la ponctuation
                    text_nettoyer = nettoyer_le_texte(lang, text)
                    prediction = tweet_classifier(text_nettoyer)
                    print('prédiction :', int(prediction[0]))
                    #outfile.write(text_nettoyer)
                    if int(prediction[0]) != 0:
                        if text_nettoyer not in self.liste_tweets_interessants:
                            self.liste_tweets_interessants.append(text_nettoyer)
                            print("/////tweet: ", json_load[structurejson1][structurejson2][structurejson3])
                            #print("texte nettoyé:", text_nettoyer)
                            print("prediction :", prediction)
                            post_tweet_elasticsearch(text, int(prediction[0]), json_load)
                            return text_nettoyer
                        else:
                            print("tweet intéssants déja vu")
                    else:
                        print("tweet non-intéréssant")
                        print(text)
                        return None


            # fonction main
            if (json_load['lang'] == "fr"):
                # test pour récupérer le texte du tweet, un tweet peut avoir une structure json différente selon son nombre de charactére, il est donc nécessaire
                # d'avoir toutes les possibilités de l'emplacement du texte du tweet
                try:
                    tweet_quoted_nettoye = get_tweets_nettoye_classifie('fr', 'quoted_status', 'extended_tweet', 'full_text')
                except KeyError:
                    tweet_quoted_nettoye = None
                try:
                    tweet_nettoye = get_tweets_nettoye_classifie('fr', 'retweeted_status', 'extended_tweet', 'full_text')
                except KeyError:
                    try:
                        tweet_nettoye = get_tweets_nettoye_classifie('fr', 'extended_tweet', 'full_text', None)
                    except KeyError:
                        tweet_nettoye = get_tweets_nettoye_classifie('fr', 'text', None, None)

            if (json_load['lang'] == "en"):
                # test pour récupérer le texte du tweet, un tweet peut avoir une structure json différente selon son nombre de charactére, il est donc nécessaire
                # d'avoir toutes les possibilités de l'emplacement du texte du tweet
                try:
                    tweet_quoted_nettoye = get_tweets_nettoye_classifie('en', 'quoted_status', 'extended_tweet', 'full_text')
                except KeyError:
                    tweet_quoted_nettoye = None
                try:
                    tweet_nettoye =get_tweets_nettoye_classifie('en', 'retweeted_status', 'extended_tweet', 'full_text')
                except KeyError:
                    try:
                        tweet_nettoye = get_tweets_nettoye_classifie('en', 'extended_tweet', 'full_text', None)
                    except KeyError:
                        tweet_nettoye =get_tweets_nettoye_classifie('en', 'text', None, None)

            # print("nombre de hashtags aquarius :" + str(compteur_hashtags))
            #enregistre les tweets en local
            '''fileName = self.fileDirectory + 'Tweets_' + dt.datetime.now().strftime(
                "%Y_%m_%d_%H") + '.json'  # File name includes date out to hour
            if tweet_quoted_nettoye is not None:
                #enregistre le fichier en local
                open(fileName, 'a').write(json.dumps(data, ensure_ascii=False))  # Append tweet to the file
            
            if tweet_nettoye is not None:
                open(fileName, 'a').write(json.dumps(data, ensure_ascii=False))  # Append tweet to the file'''


        # NB: Because the file name includes the hour, a new file is created automatically every hour.
            #en cas d'erreur enregistre les logs d'erreur en local
            '''def on_error(self, status_code, data):
                fileName = self.fileDirectory + dt.datetime.now().strftime("%Y_%m_%d_%H") + '_Errors.txt'
                open(fileName, 'a').write(json.dumps(data))'''


    # Make function.  Tracks key words.
    def streamConnect(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET):
        stream = MyStreamer(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        stream.statuses.filter(track=['Fiber Cable Link', 'subsea', 'submarine cable', 'sea cable','submarine networks', 'Singapore Cable', 'Singapore subsea cable', 'offshore manager', 'ASC', 'SACS', 'Angola Cables', 'undersea', 'deep sea', 'Fibre networks', 'subsea routes', 'superconducting cables', 'broadband investment', 'Southern Cross cable', 'submarine cable system', 'submarine power cables', 'Submarine Systems', 'wind cable', 'Offshore Wind', 'Fiber Cable', 'geotechnical', 'safnog', 'geophysical', 'geochemical', 'offshorewind', 'marine life', 'pollute beach', 'Ocean Conservation', 'pollute sea', 'pollute ocean' 'marine activities', 'endangered species', 'Marine Conservation Zones', 'protected ocean', 'underwater world', 'marine environment', 'Cable System', 'maritime sectors', 'Submarine Telecoms', 'offshore renewables industry', 'wind turbines', 'wind energy', 'offshore environment', 'offshore pipes', 'Offshore Renewable Energy', 'Offshore Services', 'store offshore', 'offshore energy', 'offshore gas', 'offshore oil', 'offshore platform' 'fishing industry', 'Sustainable fisheries', 'marine protection'], language=['fr', 'en'], stall_warnings=True)


    # Execute
    try:
        streamConnect(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    except IOError as ex:
        print("!!!just caught a error :", ex)
        time.sleep(70)
