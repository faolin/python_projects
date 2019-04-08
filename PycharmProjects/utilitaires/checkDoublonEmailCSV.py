'''Compare les mails de 2 fichiers csv pour trouver les doublons et les enlever'''
import pandas as pd
count = 0
'''compare 2 string et fais un print si elles sont égales'''
def checkForDoublon(email1, email2 ):
    if email1 == email2:
        print('Doublon found', email1)
        return True
    else:
        return False

if __name__ == '__main__':
    #file 1 doit étre le fichier contenant le plus de lignes
    file1 = '/home/francois/Téléchargements/test.csv'
    file2 = '/home/francois/Téléchargements/leads/leadsGrowLabsFD_27_03_2019_16h48.csv'
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    allEmail = []
    allFirstName = []
    allLastName = []
    allPositions = []
    allCompanies = []
    allGender = []
    for i in range(len(df1['email'])):
        email1 = df1['email'][i]
        doublon = False
        for y in range(len(df2['email'])):
            email2 = df2['email'][y]
            if checkForDoublon(email1, email2) == True:
                doublon = True
                break

        if doublon == False:
            allEmail.append(email1)
            allFirstName.append(df1['first_name'][i])
            allLastName.append(df1['last_name'][i])
            allPositions.append(df1['position'][i])
            allGender.append(df1['gender'][i])
            allCompanies.append(df1['company'][i])

    leads = pd.DataFrame({
                              'gender': allGender,
                              'position': allPositions,
                              'email': allEmail,
                              'last_name': allLastName,
                              'first_name': allFirstName,
                              'company': allCompanies
                              })
    leads.to_csv('/home/francois/Téléchargements/leadsWithoutDoublons.csv')