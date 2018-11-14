
import os
import json
import glob
import ast, sys

import requests

input_filenames =  glob.glob("/home/francois/Documents/sextant/*.json")

class geoShape():
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    type = ''
    coordinates = ''

'''transforme un array de geobox en multipolygon'''
def geoBoxToPolygon(geoBox):
    NewPolygon = geoShape()
    NewPolygon.type = 'multipolygon'
    MegaArray = []
    for i in range(len(geoBox)):
        MultiArray = []
        array = []
        split = geoBox[i].split('|')
        WestLong, EastLong, SouthLat, NorthLat = corrigeLimiteLongLat(split)
        array.append([WestLong, SouthLat])
        array.append([WestLong, NorthLat])
        array.append([EastLong, NorthLat])
        array.append([EastLong, SouthLat])
        array.append([WestLong, SouthLat])
        MultiArray.append(array)
        MegaArray.append(MultiArray)
    NewPolygon.coordinates = MegaArray
    return NewPolygon.toJSON()

def corrigeLimiteLongLat(geobox):
    '''Empéche les données géographiques de dépasser -180 et 180 en longitutue et 90 et -90 el lat'''
    if float(geobox[0]) < -180:
        WestLong = -180
    else:
        WestLong = float(geobox[0])

    if float(geobox[2]) > 180:
        EastLong = 180
    else:
        EastLong = float(geobox[2])

    if float(geobox[1]) < -90:
        SouthLat = -90
    else:
        SouthLat = float(geobox[1])

    if float(geobox[3]) > 90:
        NorthLat = 90
    else:
        NorthLat = float(geobox[3])
    return WestLong, EastLong, SouthLat, NorthLat



# merge plusieurs fichiers json en un seul et formatte les données pour envoyer le fichier sur elasticsearch
def cat_json(input_filenames):
    compteur = 0
    for infile_name in input_filenames:
        with open(infile_name) as infile:
            #aprés avoir ouvert le fichier on récupére toutes les données en texte
            infile_to_rawtext= infile.read()
            #on utlise la fonction json.loads pour pouvoir ensuite récuperer des éléments précis de la structure du fichier json
            json_load=json.loads(infile_to_rawtext, 'utf-8')
            #print(infile)
            for i in range(int(json_load['@to'])- int(json_load['@from']) ):
                #on séléctionne que les métadata dans les fichiers json
                json_selector = json_load['metadata'][i]
                compteur = compteur + 1
                presenceOfGeobox = True
                try:
                    json_selector_geo = json_selector['geoBox']
                except KeyError:
                    presenceOfGeobox = False
                #on vérifier que il y a le champs geobox dans la donnée
                if presenceOfGeobox == True:
                    location = ''
                    # Si il y a plusieurs geobox on retourne un multipolygon au lieu d'une enveloppe comme type
                    if isinstance(json_selector_geo, list) == True:
                        location = geoBoxToPolygon(json_selector_geo)
                    if isinstance(json_selector_geo, list) == False:
                        rectangle = geoShape()
                        rectangle.type = 'envelope'
                        split = json_selector_geo.split('|')
                        WestLong, EastLong, SouthLat, NorthLat = corrigeLimiteLongLat(split)
                        Array = []
                        Array.append([WestLong, NorthLat])
                        Array.append([EastLong, SouthLat])
                        rectangle.coordinates = Array
                        location = rectangle.toJSON()
                        # print(location)
                # on repasse d'un format python a un format json pour avoir les " au lieu des ' pour que elasticsearch accepte le format des données
                json_double_quote = json.dumps(json_selector, ensure_ascii=False)
                # on crée une chaine de charactére afin de pouvoir supprimer le dernier } pour ajouter la lattitude et la longitude
                string = ""
                string += str(json_double_quote)
                if presenceOfGeobox == True:
                    string_sans_crochet_a_la_fin = string[
                                                   :-1]  # supprime le dernier charactére de notre chaine de charactére
                    final_string = string_sans_crochet_a_la_fin + ',' + ' "location": {} '.format(location) + '}'
                    json_final = json.loads(final_string)
                else:
                    json_final = json.loads(string)
                print(json_final)
                url = 'http://10.20.12.67:9200/emodnet/enregistrement/'
                data = json_final
                headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                r = requests.post(url, data=json.dumps(data), headers=headers)
                print(r.text)


cat_json(input_filenames)
