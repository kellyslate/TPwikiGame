import os
import requests
from utils import get_random_wikipedia_page, get_links

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def wikirace(start_page, target_page):
    current_page = start_page
    target_title = requests.get(target_page).url.split('/')[-1]

    turns = 0

    while True:
        clear_screen()
        turns += 1
        print(f"************************ WikiGame **** tour {turns}")
        print(f"Départ : {start_page}")
        print(f"Cible : {target_page}")
        print(f"Actuellement : {current_page}")
        
        links = get_links(current_page)
        
        for i, (text, url) in enumerate(links):
            print(f"{i+1:02d} - {text}")

        print("Votre choix : ", end="")
        choice = int(input())
        
        if choice < 1 or choice > len(links):
            print("Choix invalide, veuillez réessayer.")
            continue
        
        current_page = links[choice-1][1]
        
        if current_page.split('/')[-1] == target_title:
            clear_screen()
            print(f"Félicitations ! Vous avez atteint la page cible en {turns} tours.")
            break

if __name__ == "__main__":
    start_page = get_random_wikipedia_page()
    target_page = get_random_wikipedia_page()
    wikirace(start_page, target_page)
