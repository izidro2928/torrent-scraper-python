from bs4 import BeautifulSoup
import requests
import json
import re

print('movie titles must be in English!')
print('the input below is required'.upper())
movie_input_title = input("Please Type a movie title: ".upper())
print('the input below is required'.upper())
movie_input_year = input("Please Type the movie release date: ".upper())

def yts_scraper(movie_title, movie_year):
    movie_title = movie_title.lower()
    movie_title = movie_title.replace(':', '')
    movie_title = movie_title.replace("'", "")
    movie_title = re.sub(r'[^a-zA-Z0-9]', '-', movie_title)
    print(movie_title)

    site_url = 'https://yts.mx/movies/{}-{}'.format(movie_title, movie_year)
    response = requests.get(site_url)
    source = response.text

    try:
        soup = BeautifulSoup(source, 'html.parser')
        container = soup.find('div', id='movie-info')
        container = container.find('p')
        all_links = container.find_all('a')

        links_path = {}
        for index, link in enumerate(all_links):
            link_source = link['href']
            link_title = link.text

            links_path.update({
                index: {
                    "link_source": link_source,
                    "link_title": link_title
                }
            })

        links_path = json.dumps(links_path, indent=4)
        return links_path
    except Exception:
        pass

results = yts_scraper(movie_input_title, movie_input_year)

if results:
    print("Showing Results of {}".format(movie_input_title))
    print(results)
else:
    print("Nothing was found".upper())
