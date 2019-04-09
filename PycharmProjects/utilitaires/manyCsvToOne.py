'''regroupe plusieurs fichiers csv dans un dossier en un seul et rajoute au fichier contenant toutes les emails '''
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
            for i in range (len(df['Email'])):
                allEmail.append(df['Email'])
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
    for file in inputs_filenames:
        with open(file, 'r') as infile:
            df = pd.read_csv(infile)
            print(formatFileName(file))
            for i in range(len(df['email'])):
                '''si le nouveau mail n'est pas déja dans la base alors on l'ajoute a la dataframe'''
                if checkForDoublon(df['email'][i]) == False:
                    allEmail.append(df['email'][i])
                    allFirstName.append(df['first_name'][i])
                    allLastName.append(df['last_name'][i])
                    allPositions.append(df['position'][i])
                    allScores.append(df['score'][i])
                    allCompanies.append(formatFileName(file))

'''récupére la liste des emails dans le fichier csv contenant tout les mails récupérés jusqu'ici'''
def getOldFile(file):
    with open(file, 'r') as infile:
        df = pd.read_csv(infile)
        for i in range(len(df['email'])):
                allEmail.append(df['Email'][i])
                allFirstName.append(df['first_name'][i])
                allLastName.append(df['Name'][i])
                allPositions.append(df['position'][i])
                allScores.append(df['score'][i])
                allCompanies.append(df['company'][i])

'''sauvegarde en csv la dataframe contenant les anciens et les nouveaux mails'''
def saveToCsv(FileNameSaved):
    companies = pd.DataFrame({'Contacted': None,
                              'Civilité': None,
                              'position': allPositions,
                              'Email': allEmail,
                              'Name': allLastName,
                              'first_name': allFirstName,
                              'score': allScores,
                              'Company': allCompanies
                              })
    companies = companies[['Contacted', 'Civilité', 'Name', 'Email', 'Company', 'first_name', 'position', 'score']]
    companies.to_csv(FileNameSaved, index = False)

'''permet de vérifier que parmis les nouveaux mails ne se trouvent pas des mails déja présents dans la base'''
def checkForDoublon(email):
    for i in range(len(allEmail)):
        if (email == allEmail[i]):
            print('Doublon found', email)
            return True
    return False

if __name__ == '__main__':
    allEmail = []
    allFirstName = []
    allLastName = []
    allPositions = []
    allScores = []
    allCompanies = []
    # on récupére d'abord le fichier contenant toutes les adresses mails qu'on rentre chacune dans une dataframe
    #getOldFile('/home/francois/Téléchargements/all_companies_2019_02_21_1700FFL.csv')
    # on rajoute a la dataframe les nouveaux emails récupérés
    getAllField('/home/francois/Téléchargements/allCompanies/*.csv')
    #on sauvegarde la dataframe dans un nouveau fichier csv
    saveToCsv('/home/francois/Téléchargements/all_companies.csv')
