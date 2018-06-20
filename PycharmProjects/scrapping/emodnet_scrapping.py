from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


option = webdriver.ChromeOptions()
option.add_argument("— incognito")
#option.add_argument('--headless') # permet d'afficher ou non le navigateur et ce qu'effectue commme actions le programme
option.add_argument('--no-sandbox')
browser = webdriver.Chrome(executable_path='/home/francois/Documents/chromedriver', chrome_options=option)
current_url = "http://www.emodnet.eu/geonetwork/emodnet/eng/catalog.search#/search?resultType=details&sortBy=relevance&from=1&to=20&fast=index&_content_type=json"

nbr_page_a_scrap = 5


for i in range(nbr_page_a_scrap):

    print(current_url)
    browser.get(current_url)
    browser.refresh() # on refresh la page pour qu'au début d'une nouvelle boucle on ne récupére pas les données de l'ancienne page

    timeout = 20
    # on attends que s'affiche un élément de la page pour continuer
    try:
        WebDriverWait(browser, timeout).until(
            EC.visibility_of_element_located((By.XPATH, "//div/h3/a[@class='ng-binding']")))
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()

    titles_element = browser.find_elements_by_xpath("//div/h3/a[@class='ng-binding']")


    logo_element = browser.find_elements_by_xpath("//div/ul/li/div/img[@class = 'gn-source-logo ng-scope']")


    texte_element = browser.find_elements_by_xpath("//div/p[@class = 'ng-binding']")


    image_element = browser.find_elements_by_xpath("//div[@class = 'gn-md-thumbnail']")

    # use list comprehension to get the actual repo titles and not the selenium objects.
    titles = [x.text for x in titles_element]
    logos = [y.get_attribute("src") for y in logo_element]
    texte = [x.text for x in texte_element]
    image = [y.get_attribute("src") for y in image_element]

# print out all the titles.
    print(('logos:'))
    print(logos, '\n')
    print('titles:')
    print(titles, '\n')
    print('texte:')
    print(texte, '\n')
    print('image:')
    print(image, '\n')

    # on clique sur le bouton pour aller a la page suivant, on récupere l'url de la nouvelle page
    browser.find_element_by_xpath(
        '//*[@id="ng-app"]/body/div[1]/div[4]/div[2]/div[2]/div/div[2]/div[2]/div[1]/ul[2]/li[1]/a/i').click()
    current_url = browser.current_url


