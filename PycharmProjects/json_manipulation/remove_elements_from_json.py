''' ENLEVE LES ELEMENTS PRECISES D'UNE STRUCTURE JSON'''
import json

input_filename =  'tweet_json'
liste =[]
with open(input_filename) as infile:
    infile_to_rawtext = infile.read()
    json_load = json.loads(infile_to_rawtext, 'utf-8')
    print(json_load)

    for i in json_load:
        if i!= 'retweeted': # champs a remplir si l'on veut enlever cet élément
            liste.append(i)
            liste.append(json_load[i])
print(liste)