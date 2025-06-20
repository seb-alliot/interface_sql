import sys
import os
from dotenv import load_dotenv
from pathlib import Path
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QCheckBox, QApplication
)
from PyQt6.QtCore import Qt, QTimer

from settings import (
    APP_NAME, VERSION, POSTGRESQL_AUTO_CONNECT, POSTGRES_DB, POSTGRESQL_CONFIG,
    MARIA_DB_CONFIG, MARIA_AUTO_CONNECT
)

from main.utils.regles_visuelles.fad_widjet import fade_widget
from main.utils.save_donne.config_bdd import save_bdd_config
from main.page.menu import MenuWindow
from main import center_on_screen

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

class ConfigurationWindow(QWidget):
    def __init__(self, db_type):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} - v{VERSION}")
        self.resize(600, 400)
        center_on_screen(self)
        self.setFocus()
        self.db_type = db_type
        self.inputs = {}

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Titre
        self.title_label = QLabel(f"Configuration de la base de données {db_type}.")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: black;")
        main_layout.addWidget(self.title_label)

        # Message d’info ou d’erreur
        self.message_label = QLabel("")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setStyleSheet("font-size: 14px; color: orange;")
        main_layout.addWidget(self.message_label)

        # --- Gestion type de BDD ---
        if db_type in ("PostgreSQL", "MariaDB"):
            self.checkbox_auto_connect = QCheckBox("Connexion automatique")
            if db_type == "PostgreSQL":
                self.checkbox_auto_connect.setChecked(POSTGRESQL_AUTO_CONNECT)
                config = POSTGRESQL_CONFIG()
                default_vals = POSTGRES_DB or {}
            else:  # MariaDB
                self.checkbox_auto_connect.setChecked(MARIA_AUTO_CONNECT)
                config = MARIA_DB_CONFIG()
                default_vals = config or {}

            main_layout.addWidget(self.checkbox_auto_connect, alignment=Qt.AlignmentFlag.AlignCenter)
            champs = self.generer_champs_config(config or default_vals)

            for nom_input, placeholder, echo, valeur_defaut in champs:
                champ = self.creer_input(placeholder, echo)
                if valeur_defaut:
                    champ.setText(valeur_defaut)
                champ.setObjectName(nom_input)
                self.inputs[nom_input] = champ
                main_layout.addWidget(champ, alignment=Qt.AlignmentFlag.AlignCenter)

            if champs:
                self.inputs[champs[0][0]].setFocus()

        elif db_type == "SQLite":
            self.message_label.setText("La configuration SQLite n’est pas encore disponible.")
            return

        else:
            self.message_label.setText(f"Type de BDD non reconnu : {db_type}")
            return

        # --- Boutons ---
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
        if self.db_type == "PostgreSQL":
            global POSTGRESQL_AUTO_CONNECT
            POSTGRESQL_AUTO_CONNECT = os.getenv('POSTGRESQL_AUTO_CONNECT', 'False').lower() == 'true'
            self.checkbox_auto_connect.setChecked(POSTGRESQL_AUTO_CONNECT)
        elif self.db_type == "MariaDB":
            global MARIA_AUTO_CONNECT
            MARIA_AUTO_CONNECT = os.getenv('MARIA_AUTO_CONNECT', 'False').lower() == 'true'
            self.checkbox_auto_connect.setChecked(MARIA_AUTO_CONNECT)

    def bouton_validation(self):
        dbname = self.inputs.get("bdd_name").text().strip()
        user = self.inputs.get("user").text().strip()
        password = self.inputs.get("password").text().strip()
        host = self.inputs.get("host").text().strip()
        port = self.inputs.get("port").text().strip()

        if not all([dbname, user, password, host, port]):
            self.afficher_message("Veuillez remplir tous les champs.")
            return

        try:
            port_int = int(port)
            if not (1 <= port_int <= 65535):
                raise ValueError
        except ValueError:
            self.afficher_message("Le port doit être un nombre entre 1 et 65535.")
            return

        auto_connect = self.checkbox_auto_connect.isChecked()

        if self.db_type == "PostgreSQL":
            db_config = {
                "POSTGRESQL_NAME": dbname,
                "POSTGRESQL_USER": user,
                "POSTGRESQL_PASSWORD": password,
                "POSTGRESQL_HOST": host,
                "POSTGRESQL_PORT": port_int,
                "POSTGRESQL_AUTO_CONNECT": auto_connect,
            }
        elif self.db_type == "MariaDB":
            db_config = {
                "MARIA_NAME": dbname,
                "MARIA_USER": user,
                "MARIA_PASSWORD": password,
                "MARIA_HOST": host,
                "MARIA_PORT": port_int,
                "MARIA_AUTO_CONNECT": auto_connect,
            }
        else:
            db_config = {}

        try:
            save_bdd_config(db_config)
            self.reload_config()
            self.afficher_message("Configuration enregistrée avec succès.")
            QTimer.singleShot(1000, self.retour)
        except Exception as e:
            self.afficher_message(f"Erreur lors de l'enregistrement : {e}")

    def retour(self):
        self.hide()
        self.main_window = MenuWindow(db_type=self.db_type)
        self.main_window.show()
        fade_widget(self.main_window, duration=500, fade_in=True)
        QTimer.singleShot(1000, self.deleteLater)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConfigurationWindow(db_type="PostgreSQL")
    window.show()
    sys.exit(app.exec())
