import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote, unquote

RANDOM_URL = "https://fr.wikipedia.org/wiki/Spécial:Page_au_hasard"

def get_random_wikipedia_page():
    response = requests.get(RANDOM_URL)
    return unquote(response.url)

def get_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Balises potentielles pour le contenu principal
        main_content_tags = ['div', 'main', 'article']
        
        # Recherche des liens dans les balises du contenu principal
        for tag in main_content_tags:
            content_div = soup.find(tag, {'id': 'content'})
            if content_div:
                links = content_div.find_all('a', href=True)
                break
        else:
            raise ValueError("Aucun contenu principal trouvé.")
        
        link_texts = []
        for link in links:
            href = link.get('href')
            # Filtrer les liens internes de Wikipédia
            if href.startswith('/wiki/') and ':' not in href and not href.startswith('/wiki/Wikip%C3%A9dia:'):
                full_url = urljoin("https://fr.wikipedia.org", href)
                link_texts.append((link.text, unquote(full_url)))
                if len(link_texts) == 20:  # Nous prenons les 20 premiers liens
                    break
        
        # Affichage des liens
        print(f"Links found on {url}:")
        for text, link in link_texts:
            print(f"{text}: {link}")
        
        return link_texts
    except Exception as e:
        print(f"Erreur lors de la récupération des liens : {e}")
        return []

def encode_url(url):
    return quote(url, safe=':/')
