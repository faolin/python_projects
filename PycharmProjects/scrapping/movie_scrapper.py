from bs4 import BeautifulSoup
import urllib
import pandas as pd
from time import sleep
from time import time
from random import randint
from IPython.core.display import clear_output
from warnings import warn

# https://www.dataquest.io/blog/web-scraping-beautifulsoup/

# Redeclaring the lists to store data in
names = []
years = []
imdb_ratings = []
metascores = []
votes = []

#nombre de pages a changer dans l'url (pages 1 à 2
pages = [str(i) for i in range(1,3)]
#date a changer dans l'url

years_url = [str(i) for i in range(2016,2018)] # 2016 a 2017

# Preparing the monitoring of the loop
start_time = time()
requests = 0

# For every year in the interval 2000-2017
for year_url in years_url:

    # For every page in the interval 1-4
    for page in pages:

        # Make a get request
        response = urllib.request.urlopen('http://www.imdb.com/search/title?release_date=' + year_url +
        '&sort=num_votes,desc&page=' + page)


        # Pause the loop
        sleep(randint(8, 15))

        # Monitor the requests
        requests += 1
        elapsed_time = time() - start_time
        print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
        clear_output(wait = True)

        # Throw a warning for non-200 status codes
        if response.status != 200:
            warn('Request: {}; Status code: {}'.format(requests, response.status))

        # Break the loop if the number of requests is greater than expected
        if requests > 72:
            warn('Number of requests was greater than expected.')
            break

        # Parse the content of the request with BeautifulSoup
        page_html = BeautifulSoup(response, 'html.parser')
        print(page_html)
        # Select all the 50 movie containers from a single page
        mv_containers = page_html.find_all('div', class_ = 'lister-item mode-advanced')

        # For every movie of these 50
        for container in mv_containers:
            # If the movie has a Metascore, then:
            if container.find('div', class_ = 'ratings-metascore') is not None:

                # Scrape the name
                name = container.h3.a.text
                names.append(name)

                # Scrape the year
                year = container.h3.find('span', class_ = 'lister-item-year').text
                years.append(year)

                # Scrape the IMDB rating
                imdb = float(container.strong.text)
                imdb_ratings.append(imdb)

                # Scrape the Metascore
                m_score = container.find('span', class_ = 'metascore').text
                metascores.append(int(m_score))

                # Scrape the number of votes
                vote = container.find('span', attrs = {'name':'nv'})['data-value']
                votes.append(int(vote))


# on utilise pandas pour formater les données
movie_ratings = pd.DataFrame({'movie': names,
                              'year': years,
                              'imdb': imdb_ratings,
                              'metascore': metascores,
                              'votes': votes})


#formattage des dates car il y a des (I) ou (V) a coté de certaines dates mais toujours au méme endroit on peut
#donc ne séléctionner que les 5 derniers chiffres qui contiennet la date seule

movie_ratings.loc[:, 'year'] = movie_ratings['year'].str[-5:-1].astype(int)



# affiche les meilleurs et les pires notations imdb et metascore

#movie_ratings.describe().loc[['min', 'max'], ['imdb', 'metascore']]




#permet de mettre a la méme echelle metascore et imdb ( imdb est de base noté sur 10 et metascore sur 100)

movie_ratings['n_imdb'] = movie_ratings['imdb'] * 10


#sauvegarde des données

movie_ratings.to_csv('movie_ratings.csv')




'''
names = []
years = []
imdb_ratings = []
metascores = []
votes = []


start_time = time()
requests = 0



pages = [str(i) for i in range(1,5)]
years_url = [str(i) for i in range(2000,2018)]

html = urllib.request.urlopen('http://www.imdb.com/search/title?release_date=2017&sort=num_votes,desc&page=1')
soup = BeautifulSoup(html, 'html.parser')

movie_containers = soup.find_all('div', class_ = 'lister-item mode-advanced')

for container in movie_containers:
    if container.find('div', class_ = 'ratings-metascore') is not None:



        #the name
        name = container.h3.a.text
        names.append(name)

        #years
        year= container.h3.find('span', class_ = 'lister-item-year').text
        years.append(year)

        #imdb score
        imdb = float(container.strong.text)
        imdb_ratings.append(imdb)

        #metascore
        metascore= container.find('span', class_='metascore').text
        metascores.append(int(metascore))

        #vote
        vote = container.find('span', attrs= {'name' : 'nv'})['data-value']
        votes.append(int(vote))


print(len(names), len(years), len(imdb_ratings), len(metascores), len(votes))

test_df = pd.DataFrame({'movie': names,
                       'year': years,
                       'imdb': imdb_ratings,
                       'metascore': metascores,
                       'votes': votes})
print(test_df)

#print(first_movie.find_all())

#print(first_movie)

first_name = first_movie.h3.find('span', class_ = 'lister-item-year text-muted unbold')

first_imbdb = first_movie.strong.text

first_metascore = first_movie.find('span', class_ = 'metascore')

first_vote = first_movie.find('span', attrs = {'name':'nv'})

first_vote = int(first_vote['data-value'])

eighth_movie_mscore = movie_containers[22].find('div', class_ = 'ratings-metascore')
'''