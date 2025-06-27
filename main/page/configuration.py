import sys
import os
from dotenv import load_dotenv
from pathlib import Path
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QCheckBox
)
from PyQt6.QtCore import Qt, QTimer

from settings import APP_NAME, VERSION
from main.utils.module.postgres import POSTGRESQL_CONFIG, POSTGRESQL_AUTO_CONNECT, postgresql_auto_connect
from main.utils.module.maria_db import MARIA_DB_CONFIG, MARIA_AUTO_CONNECT, maria_auto_connect
from main.utils.module.mongo_db import connect_to_mongo, MONGO_DB_CONFIG, mongo_auto_connect
from main.utils.regles_visuelles.fad_widjet import fade_widget
from main.utils.save_donne.config_bdd import save_bdd_config
from main.page.menu_principal_bdd import Menu_Principal_Window
from main import center_on_screen
from main.utils import Close

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
        self.connection = connection if connection else None
        self.inputs = {}

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

        if style_base_donné == "PostgreSQL":
            self.checkbox_auto_connect = QCheckBox("Connexion automatique")
            self.checkbox_auto_connect.setChecked(postgresql_auto_connect())
            config = POSTGRESQL_CONFIG()
            champs = self.generer_champs_config(config)

        elif style_base_donné == "MariaDB":
            self.checkbox_auto_connect = QCheckBox("Connexion automatique")
            self.checkbox_auto_connect.setChecked(maria_auto_connect())
            config = MARIA_DB_CONFIG()
            champs = self.generer_champs_config(config)

        elif style_base_donné == "MongoDB":
            self.checkbox_auto_connect = QCheckBox("Connexion automatique")
            self.checkbox_auto_connect.setChecked(mongo_auto_connect())
            config = MONGO_DB_CONFIG()
            champs = [
                ("bdd_name", "Nom de la base de données", QLineEdit.EchoMode.Normal, config.get("database", "")),
                ("user", "Nom d'utilisateur", QLineEdit.EchoMode.Normal, config.get("user", "")),
                ("password", "Mot de passe", QLineEdit.EchoMode.Password, config.get("password", "")),
                ("host", "Hôte MongoDB (cluster).exemple.mongodb.net", QLineEdit.EchoMode.Normal, config.get("host", "")),
                ("app_name", "Nom de l'app (optionnel)", QLineEdit.EchoMode.Normal, config.get("app_name", "")),
            ]

        else:
            self.message_label.setText(f"Type de BDD non reconnu : {style_base_donné}")
            return

        main_layout.addWidget(self.checkbox_auto_connect, alignment=Qt.AlignmentFlag.AlignCenter)
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
        is_default = config.get("dbname", config.get("database", "")).lower() == "default"
        return [
            ("bdd_name", "Nom de la base de données", QLineEdit.EchoMode.Normal, "" if is_default else config.get("dbname", config.get("database", ""))),
            ("user", "Nom d'utilisateur", QLineEdit.EchoMode.Normal, "" if is_default else config.get("user", "")),
            ("password", "Mot de passe", QLineEdit.EchoMode.Password, "" if is_default else config.get("password", "")),
            ("host", "Hôte de la base de données", QLineEdit.EchoMode.Normal, "" if is_default else config.get("host", "")),
            ("port", "Port de la base de données", QLineEdit.EchoMode.Normal, "" if is_default else str(config.get("port", ""))),
        ]

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
        if self.style_base_donné == "PostgreSQL":
            self.checkbox_auto_connect.setChecked(postgresql_auto_connect())
        elif self.style_base_donné == "MariaDB":
            self.checkbox_auto_connect.setChecked(maria_auto_connect())
        elif self.style_base_donné == "MongoDB":
            self.checkbox_auto_connect.setChecked(mongo_auto_connect())

    def bouton_validation(self):
        auto_connect = self.checkbox_auto_connect.isChecked()

        if self.style_base_donné == "MongoDB":
            dbname = self.inputs.get("bdd_name").text().strip()
            user = self.inputs.get("user").text().strip()
            password = self.inputs.get("password").text().strip()
            host = self.inputs.get("host").text().strip()
            app_name = self.inputs.get("app_name").text().strip() or "Cluster0"

            if not all([dbname, user, password, host]):
                self.afficher_message("Tous les champs sauf app_name sont obligatoires.")
                return

            db_config = {
                "MONGO_NAME": dbname,
                "MONGO_USER": user,
                "MONGO_PASSWORD": password,
                "MONGO_HOST": host,
                "MONGO_APP_NAME": app_name,
                "MONGO_AUTO_CONNECT": auto_connect,
            }

        elif self.style_base_donné == "PostgreSQL":
            dbname = self.inputs.get("bdd_name").text().strip()
            user = self.inputs.get("user").text().strip()
            password = self.inputs.get("password").text().strip()
            host = self.inputs.get("host").text().strip()
            port = self.inputs.get("port").text().strip()

            try:
                port_int = int(port)
                if not (1 <= port_int <= 65535):
                    raise ValueError
            except ValueError:
                self.afficher_message("Le port doit être un nombre entre 1 et 65535.")
                return

            db_config = {
                "POSTGRESQL_NAME": dbname,
                "POSTGRESQL_USER": user,
                "POSTGRESQL_PASSWORD": password,
                "POSTGRESQL_HOST": host,
                "POSTGRESQL_PORT": port_int,
                "POSTGRESQL_AUTO_CONNECT": auto_connect,
            }

        elif self.style_base_donné == "MariaDB":
            dbname = self.inputs.get("bdd_name").text().strip()
            user = self.inputs.get("user").text().strip()
            password = self.inputs.get("password").text().strip()
            host = self.inputs.get("host").text().strip()
            port = self.inputs.get("port").text().strip()

            try:
                port_int = int(port)
                if not (1 <= port_int <= 65535):
                    raise ValueError
            except ValueError:
                self.afficher_message("Le port doit être un nombre entre 1 et 65535.")
                return

            db_config = {
                "MARIA_NAME": dbname,
                "MARIA_USER": user,
                "MARIA_PASSWORD": password,
                "MARIA_HOST": host,
                "MARIA_PORT": port_int,
                "MARIA_AUTO_CONNECT": auto_connect,
            }

        else:
            self.afficher_message("Type de BDD non géré.")
            return

        try:
            save_bdd_config(db_config)
            self.reload_config()
            self.afficher_message("Configuration enregistrée avec succès.")
            QTimer.singleShot(1000, self.retour)
        except Exception as e:
            self.afficher_message(f"Erreur lors de l'enregistrement : {e}")

    def retour(self):
        self.hide()
        self.main_window = Menu_Principal_Window(
            style_base_donné=self.style_base_donné,
            connection=self.connection if self.connection else None
            )
        self.main_window.show()
        fade_widget(self.main_window, duration=500, fade_in=True)
        QTimer.singleShot(1000, self.deleteLater)

    def closeEvent(self, event):
        Close(self, event)
