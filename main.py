import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent / "main"))


# main.py
import customtkinter as ctk

from page.page_1_connection.code.connection_db import message_bienvenu, connect_to_database
from settings import APP_NAME, VERSION , DB_CONFIG

def bouton_connection():
    nom = input_pseudo.get().strip()
    if not nom:
        message_info.configure(text="Veuillez entrer un identifiant.")
        return
    password = input_password.get().strip()
    if not password:
        message_info.configure(text="Veuillez entrer un mot de passe.")
        return
    if nom == DB_CONFIG['user'] and password == DB_CONFIG['password']:
        connection = None
        try:
            connection, error = connect_to_database()
            if connection:
                message_info.configure(text=message_bienvenu(nom))
                connection.close()
            else:
                message_info.configure(text="Échec de la connexion à la base de données.")
        except Exception as e:
            message_info.configure(text=f"Identifiants incorrects.")
    else:
        message_info.configure(text="Identifiants incorrects.")

# Interface de base
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

ecran = ctk.CTk()
ecran.geometry("400x250")
ecran.title(f"{APP_NAME} - v{VERSION}")

input_pseudo = ctk.CTkEntry(ecran, placeholder_text="Entrez votre prénom")
input_pseudo.pack(pady=20)

input_password = ctk.CTkEntry(ecran, placeholder_text="Entrez votre mot de passe", show="*")
input_password.pack(pady=10)

bouton = ctk.CTkButton(ecran, text="Démarrer", command=bouton_connection)
bouton.pack()

message_info = ctk.CTkLabel(ecran, text="")
message_info.pack(pady=20)

ecran.mainloop()
