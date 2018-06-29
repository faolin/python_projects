''' LIS PLUSIEURS FICHIERS JSON DANS UN MEME DOSSIER CONTENANT DES TWEETS, NETTOIE CES TWEETS ET LES ENREGISTRE DANS UN NOUVEAU FICHIER'''

from nltk.stem.snowball import FrenchStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
import glob
import json
import nltk
import string
import re
nltk.download('stopwords')
nltk.download('punkt')
input_filenames = glob.glob("/home/francois/Documents/twitter_scrapping/*.json")
output_filename = '/home/francois/Documents/tweets_stemmises.txt'
fichier_emoticone = 'all_emoji.txt'


stemmer = FrenchStemmer()
stemmer_english = SnowballStemmer("english")
stopWords_fr = set(stopwords.words('french'))
stopWords_en = set(stopwords.words('english'))

tokenizer = TweetTokenizer(reduce_len=True, strip_handles=True, preserve_case=False) #tokenizer qui permet de transformer une phrase en une liste de mots


def remove_stopswords(language, texte_tokenize):
    wordsFiltered = []
    if(language =='fr'):
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

def remove_username_twitter(texte): # enléve les user mention et les username d'un tweet
    texte_sans_username = ""
    texte_sans_user_mention = ""

    def all_user_mention_path(texte_sans_user_mention, structurejson1, structurejson2, structurejson3):
        if structurejson3 == None :
            nbr_user_mention = len(json_load[structurejson1][structurejson2])
            struct_user_mention = json_load[structurejson1][structurejson2]
        else:
            nbr_user_mention = len(json_load[structurejson1][structurejson2][structurejson3])
            struct_user_mention = json_load[structurejson1][structurejson2][structurejson3]
        for i in range(nbr_user_mention):
            user_mention = "@" + struct_user_mention[i]['screen_name']
            if texte_sans_user_mention == "":
                elem2 = [x for x in texte.split()]
            else:
                elem2 = [x for x in texte_sans_user_mention.split()]
            for item in elem2:
                index = item.find(user_mention)
                if index != -1:
                    if texte_sans_user_mention == "":
                        texte_sans_user_mention = texte.replace(item, "")
                    else:
                        texte_sans_user_mention = texte_sans_user_mention.replace(item, "")
        return texte_sans_user_mention

    try:
        texte_sans_user_mention = all_user_mention_path(texte_sans_user_mention, 'extended_tweet', 'entities', 'user_mentions')
    except KeyError:
        result = "pas de user mention pour la structure json ci-dessus"
    try:
        texte_sans_user_mention = all_user_mention_path(texte_sans_user_mention, 'retweeted_status', 'entities', 'user_mentions')
    except KeyError:
        result = "pas de user mention pour la structure json ci-dessus"
    try:
        texte_sans_user_mention = all_user_mention_path(texte_sans_user_mention, 'entities', 'user_mentions', None)
    except KeyError:
        result = "pas de user mention pour la structure json ci-dessus"

    def all_username_path(texte_sans_username, texte_sans_user_mention, structurejson1, structurejson2,structurejson3 ):
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
            index = item.find(user_mention)
            if index != -1:
                if texte_sans_user_mention == "":
                    texte_sans_username = texte.replace(item, "")
                else:
                    texte_sans_username = texte_sans_user_mention.replace(item, "")
            else:
                if texte_sans_user_mention == "":
                    texte_sans_username = texte
                else:
                    texte_sans_username = texte_sans_user_mention
        return texte_sans_username

    try:
        texte_sans_username = all_username_path(texte_sans_username,texte_sans_user_mention,'retweeted_status', 'user','screen_name')
        return texte_sans_username
    except KeyError:
        result = "pas de user mention pour la structure json ci-dessus"
    try:
        texte_sans_username = all_username_path(texte_sans_username,texte_sans_user_mention,'in_reply_to_screen_name', None, None)
        return texte_sans_username
    except TypeError:
        if texte_sans_user_mention == "":
            return texte
        else:
            return texte_sans_user_mention


def remove_emoji(fichier_emoticone, texte):
    pas_emoticon = ""
    compteur_emote = 0
    with open(fichier_emoticone, "r") as fichier_emoticone:
        fichier_emoticone_to_rawtext = fichier_emoticone.read()
        all_emoticone = fichier_emoticone_to_rawtext.split("\n")
        for y in range(len(all_emoticone)):
            if all_emoticone[y] in texte:
                print("emote trouvée", all_emoticone[y])
                compteur_emote += 1
                if pas_emoticon == "":
                    pas_emoticon = texte.replace(all_emoticone[y], ' ')
                else:
                    pas_emoticon = pas_emoticon.replace(all_emoticone[y], ' ')
        if compteur_emote == 0 :
            print("pas d'emote détéctée.")
            return texte
        else :
            print("remove emoji: ", pas_emoticon)
            return pas_emoticon

# pas utile pour le moment
def remove_symbols(texte):

    nbr_symbol = len(json_load['entities']['symbols'])
    for i in range(nbr_symbol):
        symbol = json_load['entities']['symbols'][i]
        texte = texte.replace(symbol, " ")
    print("symbols remove:" , texte)
    return texte
def remove_punctuation(texte):
    no_punctuation = texte.translate(str.maketrans({a: " " for a in string.punctuation}))
    no_punctuation=no_punctuation.replace('’', ' ')
    no_punctuation = no_punctuation.replace('«',' ')
    no_punctuation = no_punctuation.replace('»',' ')
    no_punctuation = no_punctuation.replace('➡', ' ')
    # supprime t'on les émoticones ou on les remplaces toutes par "emoticone" afin d'étudier leur impact???
    '''
    no_punctuation = no_punctuation.replace('来', ' ')
    no_punctuation = no_punctuation.replace('自', ' ')
    no_punctuation = no_punctuation.replace('☎', ' ')
    no_punctuation = no_punctuation.replace('🌝', ' ')'''
    print("remove punctuation: ", no_punctuation)
    return no_punctuation

def nettoyer_le_texte(language, texte): # regroupement de toutes les fonctions pour nettoyer le texte
    no_url = remove_url(texte)
    no_emoji = remove_emoji(fichier_emoticone, no_url)
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

def get_tweets_nettoye_enregistre(lang,structurejson1,structurejson2, structurejson3):

    if(structurejson3 == None and structurejson2 !=None):
        print("//////tweets n°" + str(i), json_load[structurejson1][structurejson2])
        text = json_load[structurejson1][structurejson2]
        # on nettoie le texte en faisant appel a plusieurs techniques : stopwords, stemmatisation, on enléve les urls, la ponctuation
        text_nettoyer = nettoyer_le_texte(lang, text)
        print("texte nettoyé:", text_nettoyer)
        outfile.write(text_nettoyer)
    if(structurejson3 == None and structurejson2 == None ):
        print("//////tweets n°" + str(i), json_load[structurejson1])
        text = json_load[structurejson1]
        # on nettoie le texte en faisant appel a plusieurs techniques : stopwords, stemmatisation, on enléve les urls, la ponctuation
        text_nettoyer = nettoyer_le_texte(lang, text)
        print("texte nettoyé:", text_nettoyer)
        outfile.write(text_nettoyer)
    if (structurejson3 != None and structurejson2 != None):
        print("//////tweets n°" + str(i), json_load[structurejson1][structurejson2][structurejson3])
        text = json_load[structurejson1][structurejson2][structurejson3]
        # on nettoie le texte en faisant appel a plusieurs techniques : stopwords, stemmatisation, on enléve les urls, la ponctuation
        text_nettoyer = nettoyer_le_texte(lang, text)
        print("texte nettoyé:", text_nettoyer)
        outfile.write(text_nettoyer)



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

                if(json_load['lang']== "fr"):
                    # test pour récupérer le texte du tweet, un tweet peut avoir une structure json différente selon son nombre de charactére, il est donc nécessaire
                    # d'avoir toutes les possibilités de l'emplacement du texte du tweet
                    try:
                        get_tweets_nettoye_enregistre('fr','quoted_status','extended_tweet','full_text')
                    except KeyError:
                        print("pas de quoted status")
                    try:
                        get_tweets_nettoye_enregistre('fr', 'retweeted_status', 'extended_tweet', 'full_text')
                    except KeyError:
                        try:
                            get_tweets_nettoye_enregistre('fr', 'extended_tweet', 'full_text', None)
                        except KeyError:
                            get_tweets_nettoye_enregistre('fr', 'text', None, None)

                if (json_load['lang'] == "en"):
                    # test pour récupérer le texte du tweet, un tweet peut avoir une structure json différente selon son nombre de charactére, il est donc nécessaire
                    # d'avoir toutes les possibilités de l'emplacement du texte du tweet
                    try:
                        get_tweets_nettoye_enregistre('en', 'quoted_status', 'extended_tweet', 'full_text')
                    except KeyError:
                        print("pas de quoted status")
                    try:
                        get_tweets_nettoye_enregistre('en', 'retweeted_status', 'extended_tweet', 'full_text')
                    except KeyError:
                        try:
                            get_tweets_nettoye_enregistre('en', 'extended_tweet', 'full_text', None)
                        except KeyError:
                            get_tweets_nettoye_enregistre('en', 'text', None, None)

