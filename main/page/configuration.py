import os
import keyring
from dotenv import load_dotenv
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QCheckBox
from PyQt6.QtCore import Qt, QTimer

from settings import APP_NAME, VERSION
from main.utils.save_donne.config_bdd import save_bdd_config
from main.page.menu_principal_bdd import Menu_Principal_Window
from main import center_on_screen
from main.utils.fonction_diverse.import_modul import importer_module_bdd

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

class ConfigurationWindow(QWidget):
    def __init__(self, style_base_donne, connection):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} - v{VERSION}")
        self.resize(600, 400)
        center_on_screen(self)
        self.setFocus()

        self.style_base_donne = style_base_donne
        self.connection = connection
        self.inputs = {}

        try:
            self.module = importer_module_bdd(self.style_base_donne)
        except ImportError as e:
            # Pour minimalisme, on ignore l'erreur ici
            self.module = None
            return

        layout = QVBoxLayout()
        layout.setSpacing(10)  # espace vertical entre widgets

        # Titre
        label_title = QLabel(f"Configuration de la base de données {style_base_donne}.")
        label_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label_title)

        # Message d'erreur ou infos
        self.message_label = QLabel("")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.message_label)

        # Checkbox connexion auto
        self.checkbox_auto_connect = QCheckBox("Connexion automatique")
        auto_key = f"{self.style_base_donne.upper()}_AUTO_CONNECT"
        auto_connection = os.getenv(auto_key, "False").lower() == "true"
        self.checkbox_auto_connect.setChecked(auto_connection)
        layout.addWidget(self.checkbox_auto_connect, alignment=Qt.AlignmentFlag.AlignCenter)

        # Champs config
        champs = self.generer_champs_config(self.module.config())
        for key, placeholder, echo, value in champs:
            input_field = QLineEdit()
            input_field.setFixedSize(200, 30)
            input_field.setEchoMode(echo)
            input_field.setPlaceholderText(placeholder)
            input_field.setAlignment(Qt.AlignmentFlag.AlignCenter)
            if value:
                input_field.setText(value)
            input_field.setObjectName(key)
            self.inputs[key] = input_field
            layout.addWidget(input_field, alignment=Qt.AlignmentFlag.AlignCenter)

        if champs:
            self.inputs[champs[0][0]].setFocus()

        # Boutons
        btn_valider = QPushButton("Valider la configuration")
        btn_valider.setFixedSize(200, 30)
        btn_valider.clicked.connect(self.bouton_validation)
        layout.addWidget(btn_valider, alignment=Qt.AlignmentFlag.AlignCenter)

        btn_retour = QPushButton("Retour")
        btn_retour.setFixedSize(200, 30)
        btn_retour.clicked.connect(self.retour)
        layout.addWidget(btn_retour, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def generer_champs_config(self, config):
        champs = []
        service_name = f"{APP_NAME}::{self.style_base_donne}"
        mapping = {
            "dbname": ("Nom de la base de données", "DBNAME"),
            "user": ("Nom d'utilisateur", "USER"),
            "password": ("Mot de passe", "PASSWORD"),
            "host": ("Hôte", "HOST"),
            "port": ("Port", "PORT"),
            "app_name": ("Nom de l'application", "APPNAME")
        }

        for key, (placeholder, keyring_key) in mapping.items():
            value = keyring.get_password(service_name, keyring_key) or ""
            echo = QLineEdit.EchoMode.Password if "password" in key else QLineEdit.EchoMode.Normal
            champs.append((key, placeholder, echo, value))
        return champs

    def afficher_message(self, message):
        self.message_label.setText(message)

    def bouton_validation(self):
        data = {k: champ.text().strip() for k, champ in self.inputs.items()}
        auto_connect = self.checkbox_auto_connect.isChecked()

        try:
            service_name = f"{APP_NAME}::{self.style_base_donne}"

            for key, champ in self.inputs.items():
                value = champ.text().strip()
                if value:
                    keyring_key = {
                        "dbname": "DBNAME",
                        "user": "USER",
                        "password": "PASSWORD",
                        "host": "HOST",
                        "port": "PORT",
                        "app_name": "APPNAME"
                    }.get(key, key.upper())
                    keyring.set_password(service_name, keyring_key, value)

            save_bdd_config({
                f"{self.style_base_donne.upper()}_AUTO_CONNECT": auto_connect
            })

            self.afficher_message("Configuration enregistrée avec succès.")

            config = self.module.config(
                dbname=data.get("dbname"),
                user=data.get("user"),
                password=data.get("password"),
                host=data.get("host"),
                port=data.get("port"),
            )
            connection = self.module.connect(config)

            if connection:
                self.afficher_message("Connexion réussie.")
                self.connection = connection
                QTimer.singleShot(1000, self.retour)
            else:
                self.afficher_message("Échec de la connexion. Veuillez vérifier vos paramètres.")

        except Exception as e:
            self.afficher_message(f"Erreur : {e}")

    def retour(self):
        self.hide()
        self.main_window = Menu_Principal_Window(
            style_base_donne=self.style_base_donne,
            connection=self.connection,
            choix_bdd=None,
        )
        self.main_window.show()
        QTimer.singleShot(1000, self.deleteLater)
