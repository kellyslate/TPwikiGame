import requests
from bs4 import BeautifulSoup

RANDOM_URL = "https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard"

def get_random_wikipedia_page():
    response = requests.get(RANDOM_URL)
    return response.url

def get_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    content_div = soup.find('div', {'id': 'mw-content-text'})
    links = content_div.find_all('a', href=True)
    
    link_texts = []
    for link in links[:20]:  # Nous prenons les 20 premiers liens
        if link.get('href').startswith('/wiki/') and not ':' in link.get('href'):
            link_texts.append((link.text, "https://fr.wikipedia.org" + link.get('href')))
    return link_texts
