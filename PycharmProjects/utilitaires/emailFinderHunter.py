import pandas as pd
from pyhunter import PyHunter
import json
import glob
import requests


# récupére avec l'api clearbit le nom de domaine d'une company grâce a son nom
def getDomainNameFromCompany(companyName):
    import clearbit
    print('nom de la company a trouver le domaine : ', companyName)
    clearbit.key = 'sk_0e4340af79be6aba0a6940ded703eb04'
    response = clearbit.NameToDomain.find(name=companyName)
    # si l'on ne trouve pas de nom de domain l'on retourne none
    try:
        return response['domain']
    except TypeError:
        print('No domain name found, enter yours:')
        domain = input()
        return domain

'''for i in range(len(df['company'])):
    domain_search(getDomainNameFromCompany(df['company'][i]), False)'''

'''trouve a partir d'une entreprise et d'un nom l'email d'une personnne'''
def email_finder(company, name):
    print ('domain name found by clearbit:', company)
    if company is not None :
        '''You can also use the company name and the full name instead, along with raw to get the full response:'''
        hunter = PyHunter('a890302fd13f718af83604989dbd3213772a0d07')
        json_load = json.loads(hunter.email_finder(company= company, full_name= name, raw = True).text)
        email = json_load['data']['email']
        score = json_load['data']['score']
        position = json_load['data']['position']
        first_name = json_load['data']['first_name']
        last_name = json_load['data']['last_name']
        return email, score, position, first_name, last_name
    else:
        return None, None, None, None, None

'''for i in range(len(df['name'])):
    email, score = email_finder(getDomainNameFromCompany(df['company'][i]), df['name'][i])
    print(email, score)
    df['email'][i] = email
    df['score'][i] = score

df.to_csv('/home/francois/Téléchargements/resultHunterEmailFinder.csv')'''

'''permet a partir d'un nom de domaine d'une entreprise d'en ressortir des fichiers csv avec les employées de 
l'entreprise ( si qualified est true, l'on ne garde que les employés a qui l'on a trouvé le nom'''
def domain_search(company, qualified):
    if company is not None:
        hunter = PyHunter('a890302fd13f718af83604989dbd3213772a0d07')
        json_load = json.loads(hunter.domain_search(company=company, limit=1000, raw = True).text)
        positions = []
        emails = []
        last_names = []
        first_names = []
        scores = []
        companies = []
        for i in range(len(json_load['data']['emails'])):
            if emailVerifier(json_load['data']['emails'][i]['value']) == True:
                if qualified is False:
                    positions.append(json_load['data']['emails'][i]['position'])
                    emails.append(json_load['data']['emails'][i]['value'])
                    scores.append(json_load['data']['emails'][i]['confidence'])
                    last_names.append(json_load['data']['emails'][i]['last_name'])
                    first_names.append(json_load['data']['emails'][i]['first_name'])
                    companies.append(company)
                if qualified is True:
                    if json_load['data']['emails'][i]['last_name'] is not None:
                        positions.append(json_load['data']['emails'][i]['position'])
                        emails.append(json_load['data']['emails'][i]['value'])
                        scores.append(json_load['data']['emails'][i]['confidence'])
                        last_names.append(json_load['data']['emails'][i]['last_name'])
                        first_names.append(json_load['data']['emails'][i]['first_name'])
                        companies.append(company)
                if qualified is 'ultra':
                    if json_load['data']['emails'][i]['position'] is not None:
                        positions.append(json_load['data']['emails'][i]['position'])
                        emails.append(json_load['data']['emails'][i]['value'])
                        scores.append(json_load['data']['emails'][i]['confidence'])
                        last_names.append(json_load['data']['emails'][i]['last_name'])
                        first_names.append(json_load['data']['emails'][i]['first_name'])
                        companies.append(company)
        print('company name terminée: ', company)
        companies = pd.DataFrame({    'last_name': last_names,
                                      'email': emails,
                                      'company': companies,
                                      'position': positions,
                                      'first_name': first_names,
                                      'score': scores
                              })
        if emails != []:
            if qualified is False:
                companies.to_csv('/home/francois/Téléchargements/allCompanies/' + company + '.csv')
            if qualified is True:
                companies.to_csv('/home/francois/Téléchargements/allCompanies/' + company + '.csv')
            if qualified is 'ultra':
                companies.to_csv('/home/francois/Téléchargements/allCompanies/' + company + '.csv')


''' si le nom de company en contient plusieurs séparés par une , on renvoie un array avec toutes les companies, remplace
également les / par des - afin de ne pas avoir de probléme au moment de l'enregistrement du fichier avec le nom de 
company'''
def splitCompanyName(CompanyName):
    try:
        replace = CompanyName.replace('/', '-')
        return replace.split(',')
    except KeyError:
        replace = CompanyName.replace('/', '-')
        return replace


# extrait le nom de domaine d'une url
def getDomainNameFromUrl(url):
    import tldextract
    list = tldextract.extract(url)
    domain_name = list.domain + '.' + list.suffix
    return domain_name

'''for i in range(len(df['url'])):
    domainName = getDomainNameFromUrl(df['url'][i])
    domain_search(domainName, 'ultra')'''

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

#print(countEmailInDirectory("/home/francois/Téléchargements/all_companies/allcompanies_windFarmVessel/*.csv"))

'''récupére dans un dossier avec plusieurs fichiers 30 adresse mail au hasard'''
def getRandomEmail(pathTodirectory, NumberOfEmailToget):
    from random import randint
    input_filenames = glob.glob(pathTodirectory)
    allEmail = []
    while len(allEmail) < NumberOfEmailToget:
        NumberRandomFile = randint(0, len(input_filenames) - 1)
        with open(input_filenames[NumberRandomFile], 'r') as infile:
            df = pd.read_csv(infile)
            NumberRandomEmail = randint(0, len(df['emails']) - 1)
            allEmail.append((df['emails'][NumberRandomEmail]))
    emails = pd.DataFrame({'emails': allEmail})
    emails.to_csv('/home/francois/Téléchargements/emailsTest.csv')
#getRandomEmail("/home/francois/Téléchargements/allCompanies/*.csv", 30)

'''vérifier l'authencitité d'un email'''
def emailVerifier(email):
    print("email trouvé: ", email)
    if email == None:
        return False
    else:
        hunter = PyHunter('a890302fd13f718af83604989dbd3213772a0d07')
        statut = hunter.email_verifier(email)['result']
        print("statut: ", statut)
        if statut == 'undeliverable':
            return False
        else:
            return True

'''récupére une liste de tweets sur elasticsearch et retourne les noms des personnes/entreprises ayant postés ces tweets'''
def getTweetsCompanyName():
    '''GET PART'''
    url = 'http://217.182.133.71:9281/twitter/_search?source={"query": {"bool": {"must":[ {"match": {"categorie": 1}}]}}}&source_content_type=application/json&size=400&from=200'
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.get(url, headers=headers)
    json_load = json.loads(r.text)
    all_tweets = json_load['hits']['hits']
    allNames = []
    for i in range(len(all_tweets)):
        allNames.append(json.loads(all_tweets[i]['_source']['source'])['user']['name'])
    return allNames

if __name__ == '__main__':
    companies = ['vekagroup.com',
    '6s.co.za',
    'fairwater.se',
    'hmm21.com',
    'cowi.com',
    'scorpiogroup.net',
    'drewry.co.uk']
    for company in companies:
        domain_search(company, False)

    '''
    filename = "/home/francois/Téléchargements/leadstest.csv"
    df = pd.read_csv(filename)
    positions = []
    emails = []
    last_names = []
    first_names = []
    scores = []
    companies = []
    genders = []
    for i in range(len(df['first_name'])):
        name = df['first_name'][i] + ' ' + df['last_name'][i]
        print('nom de la personne: ', name)
        email, score, position, first_name, last_name = email_finder(getDomainNameFromCompany(df['company'][i]), name)
        if emailVerifier(email) == True:
            emails.append(email)
            positions.append(df['position'][i])
            first_names.append(first_name)
            last_names.append(last_name)
            scores.append(score)
            genders.append(df['gender'][i])
            companies.append(df['company'][i])

    companies = pd.DataFrame({'last_name': last_names,
                              'email': emails,
                              'company': companies,
                              'position': positions,
                              'first_name': first_names,
                              'gender': genders,
                              'score': scores
                              })
    companies.to_csv('/home/francois/Téléchargements/outputSalesNavigator1.csv')'''
