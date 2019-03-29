import gender_guesser.detector as gender
import pandas as pd
d = gender.Detector()

'''récupére la civilité a partir du prénom de la personne'''
def getGender(first_name):
    gender = d.get_gender(first_name)
    if gender == 'male':
        gender = 'Mr.'
    if gender == 'female':
        gender = 'Mrs.'
    return gender

if __name__ == '__main__':
    df1 = pd.read_csv('/home/francois/Téléchargements/testgender.csv')
    df1['gendertest'] = None
    for i in range(len(df1['first_name'])):
        df1['gender'][i] = getGender(df1['first_name'][i])

    df1.to_csv('/home/francois/Téléchargements/testgender.csv', index = False)