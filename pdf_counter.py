import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import filedialog, messagebox
import PyPDF2
import os
import re

def compter_pages_pdf(chemin_fichier):
    with open(chemin_fichier, 'rb') as fichier:
        lecteur_pdf = PyPDF2.PdfReader(fichier)
        return len(lecteur_pdf.pages)

def traiter_fichiers(chemins):
    resultats = []
    for chemin in chemins:
        nom_fichier = os.path.basename(chemin)
        if not chemin.lower().endswith('.pdf'):
            resultats.append(f"{nom_fichier} : [format non supporté]")
            continue
        try:
            nb_pages = compter_pages_pdf(chemin)
            resultats.append(f"{nom_fichier} : {nb_pages} pages")
        except Exception as e:
            resultats.append(f"{nom_fichier} : erreur ({e})")
    if resultats:
        message = "\n".join(resultats)
        show_message("Résultat", message, "info")
        set_status("Traitement terminé ✅", "green")
    else:
        show_message("Erreur", "Aucun fichier PDF valide.", "error")
        set_status("Aucun PDF ❌", "red")

def extraire_chemins(event_data):
    """Retourne une liste de chemins à partir de la chaîne dnd2."""
    if '{' in event_data and '}' in event_data:
        # Plusieurs fichiers ou chemins avec espaces
        return re.findall(r'\{([^}]*)\}', event_data)
    else:
        # Un seul fichier sans espace, ou plusieurs séparés par espace
        return event_data.split()

def drop(event):
    fichiers = event.data
    chemins = extraire_chemins(fichiers)
    traiter_fichiers(chemins)

def choisir_fichier(event=None):
    fichiers = filedialog.askopenfilenames(
        title="Sélectionner un ou plusieurs PDF",
        filetypes=[("Fichiers PDF", "*.pdf")],
        multiple=True
    )
    if fichiers:
        traiter_fichiers(fichiers)

def show_message(title, msg, type_="info"):
    if type_ == "info":
        messagebox.showinfo(title, msg)
    elif type_ == "warning":
        messagebox.showwarning(title, msg)
    else:
        messagebox.showerror(title, msg)

def set_status(msg, color):
    status_label.config(text=msg, fg=color)

# --- Flat design ---
BG = "#F7F7F7"
ACCENT = "#2563eb"
FONT = ("Segoe UI", 13)
DROP_BG = "#e0e7ff"

root = TkinterDnD.Tk()
root.title("Compteur de pages PDF")
root.geometry("370x260")
root.config(bg=BG)
root.resizable(False, False)

drop_frame = tk.Label(
    root, text="Glissez/Déposez ou Cliquez ici\npour choisir un ou plusieurs PDF",
    bg=DROP_BG, fg=ACCENT, font=("Segoe UI", 14, "bold"),
    width=32, height=5, borderwidth=0, relief="flat", cursor="hand2"
)
drop_frame.pack(pady=(28, 16))
drop_frame.drop_target_register(DND_FILES)
drop_frame.dnd_bind('<<Drop>>', drop)
drop_frame.bind("<Button-1>", choisir_fichier)

status_label = tk.Label(root, text="En attente d’un PDF...", font=FONT, bg=BG, fg="#888", pady=10)
status_label.pack()

decor = tk.Frame(root, bg="#e5e7eb", height=1)
decor.pack(fill='x', pady=(12, 0))

credits = tk.Label(
    root, text="By Hocine | PyPDF2 + TkinterDnD2", bg=BG, fg="#aaa", font=("Segoe UI", 9)
)
credits.pack(side="bottom", pady=(0, 10))

root.mainloop()
