'''Formate les données géograpghiques du catalogue d'emodnet les compare avec l'ancien datacatalogue pour eviter les redondances
 et envoie les données a un serveur elasticsearch'''
import json
import requests
input_fileName = '/home/francois/Documents/EmodnetDatacatalog.json'
fileNameToCompare = '/home/francois/Documents/DatacatalogueSansEmodnet.json'
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

with open(fileNameToCompare, 'r') as compareFile:
    rawText1 = compareFile.read()
    json_load1 = json.loads(rawText1, 'utf-8')
    json_selector1 = json_load1['hits']['hits']
    allTitles = []
    for i in range(len(json_selector1)):
        allTitles.append(json_selector1[i]['_source']['defaultTitle'])
    with open(input_fileName, 'r') as infile:
        rawText = infile.read()
        json_load = json.loads(rawText, 'utf-8')
        for i in range(len(json_load['metadata'])):
            json_selector = json_load['metadata'][i]
            #dans la boucle ci-dessous l'on vérifie si le titre est le même entre les 2 fichiers
            for y in range(len(allTitles)):
                if json_selector['defaultTitle'] == allTitles[y]:
                    copieOrNot = True
                    break
                else:
                    copieOrNot = False
            if copieOrNot == False:
                json_selector_geo = json_selector['geoBox']
                # Si il y a plusieurs geobox on retourne un multipolygon au lieu d'une enveloppe comme type
                location = ''
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
                    #print(location)
                # on repasse d'un format python a un format json pour avoir les " au lieu des ' pour que elasticsearch accepte le format des données
                json_double_quote = json.dumps(json_selector, ensure_ascii=False)
                # on crée une chaine de charactére afin de pouvoir supprimer le dernier } pour ajouter la lattitude et la longitude
                string = ""
                string += str(json_double_quote)
                string_sans_crochet_a_la_fin = string[:-1]  # supprime le dernier charactére de notre chaine de charactére
                final_string =  string_sans_crochet_a_la_fin + ',' + ' "location": {} '.format(location) + '}'
                print(final_string)
                json_final = json.loads(final_string)
                url = 'http://10.20.12.67:9200/emodnet/enregistrement/'
                data = json_final
                headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
                r = requests.post(url, data=json.dumps(data), headers=headers)
                print(r.text)
