import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
import os

#ici je vais donner les produits
produits = { #classé par cat
    "Pizza": {
        "4 fromages": 8,
        "Reine": 7,
        "Calzone": 9,
        "Napolitaine": 7,
        "Chorizo": 8,
        "Peperoni": 7,
        "Margarita": 6,
        "Hawaienne": 8,
        "Méxicaine": 9,
        "Orientale": 9,
        "Végétarienne": 7
    },
    "Dessert": {
        "Tiramisu": 4,
        "Glace": 3,
        "Brownie": 4
    },
    "Boisson": {
        "Eau": 1,
        "coca": 2,
        "Fanta": 2,
        "oasis": 2,
        "shweppes": 2,
        "ice tea": 2,
        
    }
}

commande = []       #liste cat/nom/prix
total = 0
chiffre_affaires = 0   #pour calcul du CA
nb_commandes = 0       


#def des bases
def ajouter_produit(cat, nom, prix): 
    global total
    commande.append((cat, nom, prix)) #ajout à la commande
    total += prix #maj total
    label_info.config(text=f"Ajouté : {nom} ({cat})")
    label_total.config(text=f"Total : {total} €")

def supprimer_derniere():
    global total
    if commande:
        _, _, prix = commande.pop() #suppr dernière entrée
        total -= prix #maj total
        label_info.config(text="Dernier produit supprimé.") 
        label_total.config(text=f"Total : {total} €") #maj label total
        afficher_commande() #maj affichage commande
    else:
        label_info.config(text="Aucun produit à supprimer.") #si vide

def supprimer_commande(): 
    global total, commande
    if not commande:
        messagebox.showinfo("Commande", "Aucune commande à supprimer.")
        return
    commande.clear() #vide la commande
    total = 0
    label_total.config(text="Total : 0 €")
    afficher_commande()
    label_info.config(text="Commande supprimée.")

def afficher_commande():
    if commande:
        texte = "" 
        for cat, nom, prix in commande: 
            texte += f"{cat} - {nom} : {prix} €\n" #ligne pr ligne
        texte += f"\nTotal : {total} €" #total à la fin
    else:
        texte = "Aucune commande pour l'instant."
    label_commande.config(text=texte) 

def aller_page(page):  #changer dpage
    for f in (page_accueil, page_commande, 
              page_pizza, page_dessert, page_boisson,
              page_menu, page_admin): 
        f.pack_forget() #cache toutes les pages
    page.pack(fill="both", expand=True) #aff la choisie

def imprimer_ticket():
    global chiffre_affaires, total, commande, nb_commandes
    if not commande:
        messagebox.showinfo("Ticket", "Aucune commande à imprimer.")
        return
    doc = SimpleDocTemplate("ticket.pdf", pagesize=A4) #création doc
    styles = getSampleStyleSheet() 
    story = [Paragraph("<b>Ticket de commande</b>", styles["Title"]), Spacer(1, 20)] #titre
    for cat, nom, prix in commande: #chaque ligne
        story.append(Paragraph(f"{cat} - {nom} : {prix} €", styles["Normal"])) 
    story.append(Spacer(1, 20)) #les espaces
    story.append(Paragraph(f"<b>Total : {total} €</b>", styles["Heading2"])) #total en g
    doc.build(story) #génération PDF
    messagebox.showinfo("Ticket", "Ticket PDF généré : ticket.pdf") #ptite fenetre
    chiffre_affaires += total #maj CA
    nb_commandes += 1 #maj nb commandes
    commande.clear() #vide commande
    total = 0 
    label_total.config(text="Total : 0 €") 
    afficher_commande() 
    try: 
        os.startfile("ticket.pdf") #windows
    except AttributeError:
        try:
            os.system("open ticket.pdf")  #mac
        except:
            os.system("xdg-open ticket.pdf")  #Linux

def valider_sans_ticket():  
    global chiffre_affaires, total, commande, nb_commandes
    if not commande:
        messagebox.showinfo("Commande", "Aucune commande à valider.")
        return
    chiffre_affaires += total     
    nb_commandes += 1
    commande.clear()
    total = 0
    label_total.config(text="Total : 0 €")
    afficher_commande()
    label_info.config(text="Commande validée sans ticket.")

def acces_admin():
    mdp = simpledialog.askstring("Admin", "Entrez le mot de passe :", show='*') #input mdp
    if mdp == "sofiane": #mdp admin
        label_chiffre.config(
            text=f"Chiffre d'affaires : {chiffre_affaires} €\n"
                 f"Nombre de commandes : {nb_commandes}"
        )
        aller_page(page_admin) 
    else:
        messagebox.showerror("Erreur", "Mot de passe incorrect.") #si mauvais mdp

def ajouter_menu_13():
    global total
    pizza = choix_pizza.get() #pr chaque choix menu deroulant
    dessert = choix_dessert.get()
    boisson = choix_boisson.get()
    if not pizza or not dessert or not boisson: #si un manque
        messagebox.showwarning("Menu incomplet", "Veuillez choisir une pizza, un dessert et une boisson.")
        return
    commande.append(("Menu 13€", f"{pizza} + {dessert} + {boisson}", 13)) #ajout menu
    total += 13
    label_total.config(text=f"Total : {total} €") 
    afficher_commande()  
    label_info.config(text="Menu 13€ ajouté.") 


#def de la fenettre
fenetre = tk.Tk()
fenetre.title("Prise de commande")

#Centrer la fenêtre
largeur = 700
hauteur = 500
ecran_largeur = fenetre.winfo_screenwidth()
ecran_hauteur = fenetre.winfo_screenheight()
x = int((ecran_largeur / 2) - (largeur / 2))
y = int((ecran_hauteur / 2) - (hauteur / 2))
fenetre.geometry(f"{largeur}x{hauteur}+{x}+{y}")

#dev des page en utilisant la fenetre
page_accueil = tk.Frame(fenetre)
page_commande = tk.Frame(fenetre)
page_pizza    = tk.Frame(fenetre)
page_dessert  = tk.Frame(fenetre)
page_boisson  = tk.Frame(fenetre)
page_menu     = tk.Frame(fenetre)
page_admin    = tk.Frame(fenetre)

for p in (page_accueil, page_commande, page_pizza,
          page_dessert, page_boisson, page_menu, page_admin):
    p.configure(padx=20, pady=20)

#Page Accueil
ttk.Label(page_accueil, text="so'Pizza", font=("Arial",18)).pack(pady=20)
ttk.Button(page_accueil, text="🍕 Pizza",   command=lambda: aller_page(page_pizza)).pack(pady=10)
ttk.Button(page_accueil, text="🍰 Dessert", command=lambda: aller_page(page_dessert)).pack(pady=10)
ttk.Button(page_accueil, text="🥤 Boisson", command=lambda: aller_page(page_boisson)).pack(pady=10)
ttk.Button(page_accueil, text="🍽️ Menu 13€", command=lambda: aller_page(page_menu)).pack(pady=10)
ttk.Button(page_accueil, text="🛠️ Admin",  command=acces_admin).pack(pady=10)
ttk.Button(page_accueil, text="Voir / Modifier la commande",
           command=lambda: [afficher_commande(), aller_page(page_commande)]).pack(pady=30)

#Page Commande
ttk.Label(page_commande, text="Votre commande :", font=("Arial",16)).pack(pady=10)
label_commande = ttk.Label(page_commande, text="", font=("Arial",12), justify="left")
label_commande.pack(pady=10)
ttk.Button(page_commande, text="❌ Supprimer la dernière", command=supprimer_derniere).pack(pady=10)
ttk.Button(page_commande, text="🖨️ Imprimer le ticket",    command=imprimer_ticket).pack(pady=10)
ttk.Button(page_commande, text="✅ Valider sans ticket",    command=valider_sans_ticket).pack(pady=10)
ttk.Button(page_commande, text="🗑️ Supprimer la commande", command=supprimer_commande).pack(pady=10)
ttk.Button(page_commande, text="⬅️ Retour à l'accueil",     command=lambda: aller_page(page_accueil)).pack(pady=10)

#Admin
ttk.Label(page_admin, text="Page Admin", font=("Arial",18)).pack(pady=20)
label_chiffre = ttk.Label(page_admin, text="", font=("Arial",16), justify="left")
label_chiffre.pack(pady=20)
ttk.Button(page_admin, text="⬅️ Retour à l'accueil", command=lambda: aller_page(page_accueil)).pack(pady=20)

#Menu
ttk.Label(page_menu, text="Menu complet 13€", font=("Arial",18)).pack(pady=20)


ttk.Button(page_menu, text="⬅️ Retour accueil", command=lambda: aller_page(page_accueil)).pack(pady=5)
ttk.Label(page_menu, text="Choisir une pizza :").pack()
choix_pizza = ttk.Combobox(page_menu, values=list(produits["Pizza"].keys()), state="readonly")
choix_pizza.pack(pady=5)
ttk.Label(page_menu, text="Choisir un dessert :").pack()
choix_dessert = ttk.Combobox(page_menu, values=list(produits["Dessert"].keys()), state="readonly")
choix_dessert.pack(pady=5)
ttk.Label(page_menu, text="Choisir une boisson :").pack()
choix_boisson = ttk.Combobox(page_menu, values=list(produits["Boisson"].keys()), state="readonly")
choix_boisson.pack(pady=5)
ttk.Button(page_menu, text="Ajouter le menu (13€)", command=ajouter_menu_13).pack(pady=15)
ttk.Button(page_menu, text="Voir / Modifier la commande",
           command=lambda: [afficher_commande(), aller_page(page_commande)]).pack(pady=5)

#page/cat
def creer_page_categorie(frame, categorie):
    ttk.Label(frame, text=categorie, font=("Arial",16)).pack(pady=10)  # titre
    
    # Conteneur pour la grille de boutons
    grille = tk.Frame(frame)
    grille.pack()

    col = 0
    row = 0
    #on prnd tt les produits de la cat
    for nom, prix in produits[categorie].items():
        ttk.Button(
            grille,
            text=f"{nom}\n{prix} €",
            width=15,                  #larg bouton
            command=lambda n=nom, p=prix: ajouter_produit(categorie, n, p) #ajout produit
        ).grid(row=row, column=col, padx=5, pady=5) #positionnement grille

        col += 1
        #passe a la ligne suivante tt les 3 bouton
        if col >= 3:   
            col = 0
            row += 1

    # Boutons bas de page
    ttk.Button(frame, text="⬅️ Retour accueil",
               command=lambda: aller_page(page_accueil)).pack(pady=20)
    ttk.Button(frame, text="Voir / Modifier la commande",
               command=lambda: [afficher_commande(), aller_page(page_commande)]).pack(pady=5)


creer_page_categorie(page_pizza, "Pizza") #cree les pages
creer_page_categorie(page_dessert, "Dessert")
creer_page_categorie(page_boisson, "Boisson")

#info total
label_info = ttk.Label(fenetre, text="", font=("Arial",12))
label_total = ttk.Label(fenetre, text="Total : 0 €", font=("Arial",14))
label_info.pack(side="bottom", pady=5)
label_total.pack(side="bottom", pady=5)





#init lancement
aller_page(page_accueil)
fenetre.mainloop()
