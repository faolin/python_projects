
import os
import json
import glob
import ast, sys


input_filenames =  glob.glob("/home/francois/Documents/sextant/*.json")

output_filename= "/home/francois/Documents/resultat.json"





# merge plusieurs fichiers json en un seul et formatte les données pour envoyer le fichier sur elasticsearch
def cat_json(output_filename, input_filenames):
    compteur = 0
    with open(output_filename, "w") as outfile:

        for infile_name in input_filenames:
            with open(infile_name) as infile:
                #aprés avoir ouvert le fichier on récupére toutes les données en texte
                infile_to_rawtext= infile.read()
                #on utlise la fonction json.loads pour pouvoir ensuite récuperer des éléments précis de la structure du fichier json
                json_load=json.loads(infile_to_rawtext, 'utf-8')
                print(infile)

                for i in range(int(json_load['@to'])- int(json_load['@from']) ):



                    #on séléctionne que les métadata dans les fichiers json
                    json_selector = json_load['metadata'][i]


                    #on fait un try pour gérer les cas ou l'enregistrement n'a pas d'attribut geobox
                    try:
                        # on séléctionne que les coordonnées géographiques dans le fichier json
                        lat_centrale = 0.000
                        long_centrale = 0.000
                        json_selector_geo = json_selector['geoBox']

                        #print(json_selector)

                        #on fait un try pour gérer les cas ou il y a plusieurs geobox au lieu d'une seule dans l'enregistrement
                        try:

                            json_selector_split = json_selector_geo.split('|')

                            # on calcule les longitudes et latitude centrales de la geobox

                            lat_centrale = (float(json_selector_split[0]) + float(json_selector_split[2])) / 2
                            long_centrale = (float(json_selector_split[1]) + float(json_selector_split[3])) / 2
                            #print(lat_centrale)
                            #print(long_centrale)

                        except AttributeError:
                            # lat_centrale = 0
                            # long_centrale = 0
                            for i in range(len(json_selector_geo)):
                                json_selector_split = json_selector_geo[i].split('|')

                                lat_centrale = lat_centrale + (
                                            float(json_selector_split[0]) + float(json_selector_split[2])) / 2
                                long_centrale = long_centrale + (
                                            float(json_selector_split[1]) + float(json_selector_split[3])) / 2


                            lat_centrale = lat_centrale / len(json_selector_geo)
                            long_centrale = long_centrale / len(json_selector_geo)
                            #print(lat_centrale)
                            #print(long_centrale)


                    except KeyError:

                        lat_centrale = None
                        long_centrale = None
                        #print(long_centrale)
                        #print(lat_centrale)


                    compteur = compteur + 1
                    #on repasse d'un format python a un format json pour avoir les " au lieu des ' pour que elasticsearch accepte le format des données
                    json_double_quote = json.dumps(json_selector, ensure_ascii=False)

                    #on crée une chaine de charactére afin de pouvoir supprimer le dernier } pour ajouter la lattitude et la longitude
                    string = ""
                    string += str(json_double_quote)
                    string_sans_crochet_a_la_fin = string[:-1] #supprime le dernier charactére de notre chaine de charactére

                    json_final = string_sans_crochet_a_la_fin + ','+ ' "location": "{}, {}" ' .format(lat_centrale, long_centrale) +'}'

                    print(json_final)

                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    #bien penser a mettre le même nom d'index que celui sur elasticsearch si l'on souhaite importer les données dans l'index déja crée
                    outfile.write('{"index": {"_index": "result2", "_type": "enregistrement", "_id": %d}}'%compteur + '\n')
                    outfile.write(str(json_final) + '\n')





cat_json(output_filename, input_filenames)


