'''filtre un fichier csv en fonction d'une de ses colonnes avec une autre colonne contenant les mots intérésant avec lesquels filtrer'''
import pandas as pd

filename = "/home/francois/Téléchargements/all_companies_with_researched positions_2019_02_04.csv"
df = pd.read_csv(filename)

emails = []
company = []
lastNames = []
firstNames =[]
positions = []
scores = []

for y in range(len(df['position'])):
    for i in range(len(df['positionInteressante'])):
        if (df['positionInteressante'][i] == df['position'][y]):
            isItInterssant = True
            break
        else:
            isItInterssant = False
    if isItInterssant == False:
        print('position non-intéréssante', df['positionInteressante'][i], df['position'][y] )
    else:
        print('position intéréssante', df['positionInteressante'][i], df['position'][y] )
        emails.append(df['emails'][y])
        positions.append(df['position'][y])
        lastNames.append(df['last_name'][y])
        firstNames.append(df['first_name'][y])
        company.append(df['company'][y])
        scores.append(df['score'][y])

companies = pd.DataFrame({ 'position': positions,
                                  'emails': emails,
                                  'last_name': lastNames,
                                  'first_name': firstNames,
                                   'company': company,
                                  'score': scores,

                          })

companies.to_csv('/home/francois/Téléchargements/emailsTest.csv')