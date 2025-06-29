import sys
import os
from dotenv import load_dotenv
from pathlib import Path
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QCheckBox
from PyQt6.QtCore import Qt, QTimer

from settings import APP_NAME, VERSION
from main.utils.regles_visuelles.fad_widjet import fade_widget
from main.utils.save_donne.config_bdd import save_bdd_config
from main.page.menu_principal_bdd import Menu_Principal_Window
from main.utils import Close
from main import center_on_screen
from main.utils.fonction_diverse.import_modul import importer_module_bdd

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

class ConfigurationWindow(QWidget):
    def __init__(self, style_base_donné, connection):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} - v{VERSION}")
        self.resize(600, 400)
        center_on_screen(self)
        self.setFocus()

        self.style_base_donné = style_base_donné
        self.connection = connection
        self.inputs = {}

        try:
            self.module = importer_module_bdd(self.style_base_donné)
        except ImportError as e:
            self.module = None
            self.message_label.setText(str(e))
            return

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title_label = QLabel(f"Configuration de la base de données {style_base_donné}.")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: black;")
        main_layout.addWidget(self.title_label)

        self.message_label = QLabel("")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setStyleSheet("font-size: 14px; color: orange;")
        main_layout.addWidget(self.message_label)

        self.checkbox_auto_connect = QCheckBox("Connexion automatique")
        auto_key = f"{self.style_base_donné.upper()}_AUTO_CONNECT"
        auto_connection= os.getenv(auto_key, "False").lower() == "true"
        self.checkbox_auto_connect.setChecked(auto_connection)
        main_layout.addWidget(self.checkbox_auto_connect, alignment=Qt.AlignmentFlag.AlignCenter)

        # On récupère dynamiquement la config
        champs = self.generer_champs_config(self.module.config())

        for nom_input, placeholder, echo, valeur_defaut in champs:
            champ = self.creer_input(placeholder, echo)
            if valeur_defaut:
                champ.setText(valeur_defaut)
            champ.setObjectName(nom_input)
            self.inputs[nom_input] = champ
            main_layout.addWidget(champ, alignment=Qt.AlignmentFlag.AlignCenter)

        if champs:
            self.inputs[champs[0][0]].setFocus()

        self.validation_button = QPushButton("Valider la configuration")
        self.validation_button.setFixedSize(200, 30)
        self.validation_button.clicked.connect(self.bouton_validation)
        main_layout.addWidget(self.validation_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.retour_button = QPushButton("Retour")
        self.retour_button.setFixedSize(200, 30)
        self.retour_button.clicked.connect(self.retour)
        main_layout.addWidget(self.retour_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)

    def generer_champs_config(self, config):
        # Adaptation générique (PostgreSQL, MariaDB, MongoDB)
        champs = []

        # Liste probable des champs pour tous types de base de données
        mapping = {
            "bdd_name": ("Nom de la base de données", "dbname", "database"),
            "user": ("Nom d'utilisateur", "user"),
            "password": ("Mot de passe", "password"),
            "host": ("Hôte", "host"),
            "port": ("Port", "port"),
            "app_name": ("Nom de l'application", "app_name")
        }

        for key, (placeholder, *aliases) in mapping.items():
            value = ""
            for alias in aliases:
                if alias in config:
                    value = str(config[alias])
                    break
            # on transforme le champs en étoiles
            echo = QLineEdit.EchoMode.Password if "password" in key else QLineEdit.EchoMode.Normal
            champs.append((key, placeholder, echo, value))

        return champs

    def creer_input(self, placeholder, echo_mode):
        champ = QLineEdit()
        champ.setFixedSize(200, 30)
        champ.setEchoMode(echo_mode)
        champ.setPlaceholderText(placeholder)
        champ.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return champ

    def afficher_message(self, message):
        self.message_label.setText(message)

    def reload_config(self):
        load_dotenv(dotenv_path=dotenv_path, override=True)

    def bouton_validation(self):
        data = {key: champ.text().strip() for key, champ in self.inputs.items()}
        auto_connect = self.checkbox_auto_connect.isChecked()

        try:
            save_bdd_config({
                **{f"{self.style_base_donné.upper()}_{k.upper()}": v for k, v in data.items()},
                f"{self.style_base_donné.upper()}_AUTO_CONNECT": auto_connect
            })
            self.reload_config()
            self.afficher_message("Configuration enregistrée avec succès.")
            QTimer.singleShot(1000, self.retour)
        except Exception as e:
            self.afficher_message(f"Erreur lors de l'enregistrement : {e}")

    def retour(self):
        self.hide()
        self.main_window = Menu_Principal_Window(
            style_base_donné=self.style_base_donné,
            connection=self.connection,
            choix_bdd=None,
        )
        self.main_window.show()
        fade_widget(self.main_window, duration=500, fade_in=True)
        QTimer.singleShot(1000, self.deleteLater)

    def closeEvent(self, event):
        Close(self, event)
