import json
import pandas as pd



infile_name = "/home/francois/Documents/twitter_scrapping/Tweets_2018_06_11_16.json"

defaultabstract_list = []
credit_list = []
defaultTitle_list = []

with open(infile_name) as infile:
    # aprés avoir ouvert le fichier on récupére toutes les données en texte
    infile_to_rawtext = infile.read()

    # on utlise la fonction json.loads pour pouvoir ensuite récuperer des éléments précis de la structure du fichier json
    json_load = json.loads(infile_to_rawtext, 'utf-8')
    # !!!! si il y a une erreur penser a rajouter des { au début et a la fin du fichier
    print("test")

    for i in range(4000):



        try:
            # on appelle la colonne abstract dans la structure json qui est une sous colonne de "_source" qui est une sous colonne de "hits" qui est ...
            defaultabstract = json_load['hits']['hits'][i]['_source']['abstract']
            abstract_double_quote = json.dumps(defaultabstract, ensure_ascii=False)
            defaultabstract_list.append(abstract_double_quote)




        except KeyError:

            defaultabstract_list.append("Null")


        try:
            credit = json_load['hits']['hits'][i]['_source']['credit']
            credit_list.append(credit)

        except KeyError:
            credit_list.append("Null")

        try:
            defaultTitle = json_load['hits']['hits'][i]['_source']['defaultTitle']
            defaultTitle_list.append(defaultTitle)

        except KeyError:
            defaultTitle_list.append("Null")

print(len(defaultTitle_list), len(credit_list), len(defaultabstract_list))
# on utilise pandas pour formater les données
data_catalogue = pd.DataFrame({'defaultTitle': defaultTitle_list,
                              'credit': credit_list,
                              'defaultabstract': defaultabstract_list
                              })


#sauvegarde des données

data_catalogue.to_csv('/home/francois/data_catalogue.csv')