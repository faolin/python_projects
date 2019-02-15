from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd

option = webdriver.ChromeOptions()
option.add_argument("— incognito")
#option.add_argument('--headless') # permet d'afficher ou non le navigateur et ce qu'effectue commme actions le programme
option.add_argument('--no-sandbox')
browser = webdriver.Chrome(executable_path='/home/francois/Documents/chromedriver', chrome_options=option)
current_url = "https://connect.jujama.com/AdvancedSearch/People.aspx?From=Master"

userid = '*****'
password = '****'


'''fait attendre le browser jusqu'a qu'un element soit affiché a l'écran'''

def waitLoadElement(xpath):
    timeout = 20
    try:
        WebDriverWait(browser, timeout).until(
            EC.visibility_of_element_located((By.XPATH, xpath )))
        print('waited')
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()

'''permet d'attendre la fin d'un loader avant de continuer le scrapping'''

def waitLoaderToDisappear(xpath):
    SHORT_TIMEOUT = 5  # give enough time for the loading element to appear
    LONG_TIMEOUT = 10  # give enough time for loading to finish
    LOADING_ELEMENT_XPATH = xpath
    try:
        # wait for loading element to appear
        # - required to prevent prematurely checking if element
        #   has disappeared, before it has had a chance to appear
        WebDriverWait(browser, SHORT_TIMEOUT
                      ).until(EC.presence_of_element_located((By.XPATH, LOADING_ELEMENT_XPATH)))
        # then wait for the element to disappear
        WebDriverWait(browser, LONG_TIMEOUT
                      ).until_not(EC.presence_of_element_located((By.XPATH, LOADING_ELEMENT_XPATH)))
    except TimeoutException:
        # if timeout exception was raised - it may be safe to
        # assume loading has finished, however this may not
        # always be the case, use with caution, otherwise handle
        # appropriately.
        pass
'''fait patienter le driver jusqu'a ce que la valeur d'un champs soit égale a la valeur précisée'''

def waitValueElement(xpath, value):
    timeout = 20
    try:
        WebDriverWait(browser, timeout).until(
            EC.text_to_be_present_in_element_value((By.XPATH, xpath), value))
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()

'''remplissage automatique du champs login et mot de passe'''

def connexion():
    browser.find_element_by_xpath('//*[@id="txtUserName"]').send_keys(userid)
    browser.find_element_by_xpath('//*[@id="txtPassword"]').send_keys(password)
    browser.find_element_by_xpath('//*[@id="btnLogin"]').click()
    #on clique sur le bouton continue ensuite
    #browser.find_element_by_xpath('// *[ @ id = "hlnkContinue"]').click()

'''change la page actuelle et recharge la nouvelle page pour avoir le nouveau html'''

def changePage(url):
    browser.get(url)
    browser.refresh()

'''clique sur un boutton grace a son xpath'''
def clickButton(xpath):
    browser.find_element_by_xpath(xpath).click()

'''rempli un input avec une valeur donnée grace a son xpath'''

def input(xpath, value):
    browser.find_element_by_xpath(xpath).clear()
    browser.find_element_by_xpath(xpath).send_keys(value)


'''permet de passer a la page suivante en remplissant l'input par le numéro de page ou l'on veut aller
  et clicker sur le bouton go permettant de changer de page'''

def nextPage(PageNumberToGo):
    input('//*[@id="cphMain_CustomPager2_txtPage"]', str(PageNumberToGo))
    clickButton('//*[@id="cphMain_CustomPager2_lnkGotopages"]')


''' récupére les valeurs des champs de la table'''

def getPersonInfos(nbr_personne_par_page, nbr_page):
    #on rajoute 2 car l'on commence a changer de page a partir de la page 2
    names = []
    company = []
    position = []
    for i in range(2, nbr_page):
        for y in range(nbr_personne_par_page):
            name_elements = browser.find_element_by_xpath(
                '//*[@id="cphMain_ucPeople_rptPeopleTableView_hlnkPersonName_' + str(y) + '"]')
            company_elements = browser.find_element_by_xpath(
                '//*[@id="cphMain_ucPeople_rptPeopleTableView_tdCompany_' + str(y) + '"]')
            position_elements = browser.find_element_by_xpath(
                '//*[@id="cphMain_ucPeople_rptPeopleTableView_lblJobTitle_' + str(y) + '"]')
            names.append(name_elements.text)
            company.append(company_elements.text)
            position.append(position_elements.text)
        "on passe a la page suivante"
        nextPage(i)
        waitLoaderToDisappear('//*[@id="loaddiv"]')
    return names, company, position

'''sauvegarde au format csv '''
def saveToCsv(names, company, position):
    # on utilise pandas pour formater les données
    catalgogue_emodnet = pd.DataFrame({'name': names,
                                       'company': company,
                                       'position': position,
                                       })
    catalgogue_emodnet.to_csv('/home/francois/Documents/londesBDD.csv')
if __name__ == '__main__':
    changePage(current_url)
    #on attends que le formulaire de connexion soit affiché pour remplir les champs login et mdp
    waitLoadElement('//*[@id="content"]')
    connexion()
    #une fois connecté on peut aller directement a la page qui nous intérésse
    changePage('https://connect.jujama.com/AdvancedSearch/People.aspx?From=Master')
    #on clique sur le boutton pour passer a la table view
    clickButton('// *[ @ id = "cphMain_ucPeople_liTableView"]')
    # on attends que la table des personnes avec leurs noms ait finie de charger avant de continuer
    waitLoadElement('//*[@id="cphMain_ucPeople_rptPeopleTableView_hlnkPersonName_0"]')
    #on lance la recherche de personne
    names, company, position = getPersonInfos(10, 33)
    saveToCsv(names, company, position)

