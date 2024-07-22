import os
import requests
import tkinter as tk
from tkinter import messagebox
from utils import get_random_wikipedia_page, get_links, encode_url

# Utilisation de la bibliothèque tkinter pour le rendu graphique.
class WikiGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WikiGame")
        self.geometry("1920x1080")
        
        # Initialisation des pages de départ, cible et actuelle
        self.start_page = get_random_wikipedia_page()
        self.target_page = get_random_wikipedia_page()
        self.current_page = self.start_page
        
        # Initialisation du compteur de tours + Création des widgets + Maj des liens affichés
        self.turns = 0
        self.link_offset = 0
        self.links = []
        self.create_widgets()
        self.update_links()

    def create_widgets(self):
        # Nombre de tours
        self.turn_label = tk.Label(self, text=f"Tour : {self.turns}")
        self.turn_label.pack()
        
        # Page de départ
        self.start_label = tk.Label(self, text=f"Départ : {self.start_page}")
        self.start_label.pack()
        
        # Page cible
        self.target_label = tk.Label(self, text=f"Cible : {self.target_page}")
        self.target_label.pack()
        
        # Page actuelle
        self.current_label = tk.Label(self, text=f"Actuellement : {self.current_page}")
        self.current_label.pack()
        
        # Cadre pour les liens hypertextes
        self.links_frame = tk.Frame(self, width=800, height=600)  
        self.links_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.links_frame.pack_propagate(False)
        
        # Cadre pour les boutons de navigation, centré en dessous des liens
        self.nav_frame = tk.Frame(self)
        self.nav_frame.place(relx=0.5, rely=0.9, anchor=tk.CENTER)
        
        # Bouton pour les liens précédents
        self.prev_button = tk.Button(self.nav_frame, text="Liens précédents", command=self.prev_links, state=tk.DISABLED)
        self.prev_button.grid(row=0, column=0, padx=5)
        
        # Bouton pour les liens suivants
        self.next_button = tk.Button(self.nav_frame, text="Liens suivants", command=self.next_links, state=tk.DISABLED)
        self.next_button.grid(row=0, column=1, padx=5)

    def update_links(self):
        # Suppression des widgets enfants existants dans le cadre des liens
        for widget in self.links_frame.winfo_children():
            widget.destroy()
        
        # Incrémentation du compteur de tours
        self.turns += 1
        self.turn_label.config(text=f"Tour : {self.turns}")
        self.current_label.config(text=f"Actuellement : {self.current_page}")

        # Récupération des liens
        self.links = get_links(self.current_page)
        
        # Message d'erreur s'il n'y a pas de liens
        if not self.links:
            messagebox.showerror("Erreur", "Aucun lien trouvé sur cette page.")
            return
        
        # Affichage des liens par paquets de 20
        self.display_links()

    def display_links(self):
        # Suppression des widgets enfants existants dans le cadre des liens
        for widget in self.links_frame.winfo_children():
            widget.destroy()
        
        # Afficher les liens de la page actuel
        for link in self.links[self.link_offset:self.link_offset + 20]:
            text, url = link
            btn = tk.Button(self.links_frame, text=text, command=lambda url=url: self.on_link_click(url), width=100)  # Fixe la largeur du bouton
            btn.pack(fill=tk.X)
        
        # Mise à jour de l'état des boutons de navigation
        self.prev_button.config(state=tk.NORMAL if self.link_offset > 0 else tk.DISABLED)
        self.next_button.config(state=tk.NORMAL if self.link_offset + 20 < len(self.links) else tk.DISABLED)

    def next_links(self):
        # Afficher les 20 liens suivants
        if self.link_offset + 20 < len(self.links):
            self.link_offset += 20
            self.display_links()

    def prev_links(self):
        # Afficher les 20 liens précédents
        if self.link_offset >= 20:
            self.link_offset -= 20
            self.display_links()

    def on_link_click(self, url):
        # Maj après clic sur un lien
        self.current_page = url
        self.link_offset = 0  # Réinitialiser l'offset des liens
        self.current_label.config(text=f"Actuellement : {self.current_page}")
        
        # Vérification si la page actuelle est la page cible
        target_title = requests.get(self.target_page).url.split('/')[-1]
        if self.current_page.split('/')[-1] == target_title:
            messagebox.showinfo("Félicitations !", f"Vous avez atteint la page cible en {self.turns} tours.")
            self.destroy()
        else:
            self.update_links()

if __name__ == "__main__":
    app = WikiGame()
    app.mainloop()
