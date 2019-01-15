'''regroupe plusieurs fichiers csv dans un dossier en un seul'''
import glob
import pandas as pd
import os
'''compte le nombre d'email dans la colonne mail de plusieurs fichiers csv présent dans un méme dossier'''
def countEmailInDirectory(path):
    input_filenames =  glob.glob(path)
    allEmail = []
    for file in input_filenames:
        with open(file, 'r') as fileSee:
            df = pd.read_csv(fileSee)
            for i in range (len(df['emails'])):
                allEmail.append(df['emails'])
    return len(allEmail)

'''récupére le path d'un fichier csv, enléve le chemin d'accés et supprime l'extension .csv a la fin pour ne garder
seulement le nom de companie'''
def formatFileName(file):
    split = file.split('/')
    companyName = '.'.join(split[5].split('.')[:-1])
    return companyName
'''récupére tout les champs des tout les fichiers présents dans un dossier et les merge dans un seul fichier'''
def getAllField(path):
    inputs_filenames = glob.glob(path)
    allEmail = []
    allFirstName = []
    allLastName = []
    allPositions = []
    allScores = []
    allCompanies = []
    for file in inputs_filenames:
        with open(file, 'r') as infile:
            df = pd.read_csv(infile)
            for i in range(len(df['emails'])):
                allEmail.append(df['emails'][i])
                allFirstName.append(df['first_name'][i])
                allLastName.append(df['last_name'][i])
                allPositions.append(df['position'][i])
                allScores.append(df['score'][i])
                allCompanies.append(formatFileName(file))
    print(allCompanies)
    companies = pd.DataFrame({'position': allPositions,
                              'emails': allEmail,
                              'last_name': allLastName,
                              'first_name': allFirstName,
                              'score': allScores,
                              'company': allCompanies
                              })
    companies.to_csv('/home/francois/Téléchargements/all_companies.csv')
getAllField('/home/francois/Téléchargements/all_csv/*.csv')
#print(countEmailInDirectory('/home/francois/Téléchargements/all_csv/*.csv'))