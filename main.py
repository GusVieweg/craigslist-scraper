import requests
import re
import concurrent.futures
from bs4 import BeautifulSoup

keywords = ['web', 'dev', 'development', 'video', 'film', 'vid', 'shoot', 'record']

def get_gigs(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    return soup.find_all('p', class_='result-info')

def print_gigs(gigs, keywords):
    for gig in gigs:
        gig_a_tag = gig.find('a', class_="result-title")
        for word in keywords:
          if word in gig_a_tag.text.lower():
            time = gig.find('time').text
            job = gig_a_tag.text
            link = gig_a_tag.attrs['href']
            location = "not listed"
            try:
                regex = re.compile(f"\/d\/(\S+)\-{job.split(' ')[0].lower()}")
                location = re.search(regex, link).group(1)
            except:
                pass
            print(f'{time}: {job} ({location}) -- {link}')
            break

URLS = [
    'https://raleigh.craigslist.org/d/tv-film-video-radio/search/tfr',
    'https://raleigh.craigslist.org/d/creative-gigs/search/crg'
    ]

gigs = []
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    futures = [executor.submit(get_gigs, url) for url in URLS]
    gigs = []
    for result in concurrent.futures.as_completed(futures):
        gigs.extend(result.result())


print_gigs(gigs, keywords)
