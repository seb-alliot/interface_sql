import sys
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=dotenv_path)
from pathlib import Path
from settings import APP_NAME, VERSION, POSTGRESQL_AUTO_CONNECT, POSTGRES_DB, POSTGRESQL_CONFIG

sys.path.append(str(Path(__file__).resolve().parent / "main"))

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QCheckBox, QApplication
)
from PyQt6.QtCore import Qt, QTimer

from main.utils.regles_visuelles.fad_widjet import fade_widget
from main.utils.save_donne.config_bdd import save_bdd_config
from main.page.page_2_menu.menu import MenuWindow
from main import center_on_screen


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

        # Champs inputs pour PostgreSQL
        if db_type == "PostgreSQL":
            self.checkbox_auto_connect = QCheckBox("Connexion automatique")
            self.checkbox_auto_connect.setChecked(POSTGRESQL_AUTO_CONNECT)
            main_layout.addWidget(self.checkbox_auto_connect, alignment=Qt.AlignmentFlag.AlignCenter)

            # Récupération config actuelle
            self.postgres_config = POSTGRESQL_CONFIG()

            # Valeurs par défaut
            def_valeurs = {}
            if self.postgres_config and self.postgres_config.get("dbname"):
                def_valeurs = self.postgres_config
            else:
                def_valeurs = POSTGRES_DB or {}
            if self.postgres_config.get("dbname") == "default":
                champs = [
                    ("bdd_name", "Nom de la base de données", QLineEdit.EchoMode.Normal, ""),
                    ("user", "Nom d'utilisateur", QLineEdit.EchoMode.Normal, ""),
                    ("password", "Mot de passe", QLineEdit.EchoMode.Password, ""),
                    ("host", "Hôte de la base de données", QLineEdit.EchoMode.Normal, ""),
                    ("port", "Port de la base de données", QLineEdit.EchoMode.Normal, ""),
                ]
            else:
                champs = [
                    ("bdd_name", "Nom de la base de données", QLineEdit.EchoMode.Normal, def_valeurs.get("dbname", "")),
                    ("user", "Nom d'utilisateur", QLineEdit.EchoMode.Normal, def_valeurs.get("user", "")),
                    ("password", "Mot de passe", QLineEdit.EchoMode.Password, def_valeurs.get("password", "")),
                    ("host", "Hôte de la base de données", QLineEdit.EchoMode.Normal, def_valeurs.get("host", "")),
                    ("port", "Port de la base de données", QLineEdit.EchoMode.Normal, str(def_valeurs.get("port", ""))),
                ]

            for nom_input, placeholder, echo, valeur_defaut in champs:
                champ = self.creer_input(placeholder, echo)
                if valeur_defaut:
                    champ.setText(valeur_defaut)
                champ.setObjectName(nom_input)
                self.inputs[nom_input] = champ
                main_layout.addWidget(champ, alignment=Qt.AlignmentFlag.AlignCenter)

            # Focus automatique sur le premier champ
            if champs:
                self.inputs[champs[0][0]].setFocus()

        # Boutons
        self.validation_button = QPushButton("Valider la configuration")
        self.validation_button.setFixedSize(200, 30)
        self.validation_button.clicked.connect(self.bouton_validation)
        main_layout.addWidget(self.validation_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.retour_button = QPushButton("Retour")
        self.retour_button.setFixedSize(200, 30)
        self.retour_button.clicked.connect(self.retour)
        main_layout.addWidget(self.retour_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)

    def reload_config(self):
        load_dotenv()
        global POSTGRESQL_AUTO_CONNECT
        POSTGRESQL_AUTO_CONNECT = os.getenv('POSTGRESQL_AUTO_CONNECT', 'False').lower() == 'true'
        self.checkbox_auto_connect.setChecked(POSTGRESQL_AUTO_CONNECT)

    def retour(self):
        self.hide()
        self.main_window = MenuWindow(db_type=self.db_type)
        self.main_window.show()
        fade_widget(self.main_window, duration=500, fade_in=True)
        QTimer.singleShot(1000, self.deleteLater)

    def creer_input(self, placeholder, echo_mode):
        champ = QLineEdit()
        champ.setFixedSize(200, 30)
        champ.setEchoMode(echo_mode)
        champ.setPlaceholderText(placeholder)
        champ.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return champ

    def bouton_validation(self):
        # Récupération des valeurs saisies
        dbname = self.inputs.get("bdd_name").text().strip() if self.inputs.get("bdd_name") else ""
        user = self.inputs.get("user").text().strip() if self.inputs.get("user") else ""
        password = self.inputs.get("password").text().strip() if self.inputs.get("password") else ""
        host = self.inputs.get("host").text().strip() if self.inputs.get("host") else ""
        port = self.inputs.get("port").text().strip() if self.inputs.get("port") else ""

        # Validation champs remplis
        if not all([dbname, user, password, host, port]):
            self.afficher_message("Veuillez remplir tous les champs.")
            return

        # Validation port
        try:
            port_int = int(port)
            if not (1 <= port_int <= 65535):
                raise ValueError
        except ValueError:
            self.afficher_message("Le port doit être un nombre entre 1 et 65535.")
            return

        auto_connect = self.checkbox_auto_connect.isChecked()

        # Construction de la config
        if self.db_type == "PostgreSQL":
            db_config = {
                "POSTGRESQL_NAME": dbname,
                "POSTGRESQL_USER": user,
                "POSTGRESQL_PASSWORD": password,
                "POSTGRESQL_HOST": host,
                "POSTGRESQL_PORT": port_int,
                "POSTGRESQL_AUTO_CONNECT": auto_connect,
            }
        else:
            db_config = {
                "DB_NAME": dbname,
                "DB_USER": user,
                "DB_PASSWORD": password,
                "DB_HOST": host,
                "DB_PORT": port_int,
                "DB_AUTO_CONNECT": auto_connect,
            }

        # Enregistrement config
        try:
            save_bdd_config(db_config)  # sauvegarde dans .env

            from dotenv import load_dotenv
            load_dotenv(override=True)  # recharge le .env avec les nouvelles valeurs

            self.reload_config()
            self.afficher_message("Configuration enregistrée avec succès.")
            QTimer.singleShot(1000, self.apres_validation)

        except Exception as e:
            self.afficher_message(f"Erreur lors de l'enregistrement : {e}")

    def apres_validation(self):
        if self.db_type == "PostgreSQL":
            if hasattr(self, "checkbox_auto_connect"):
                auto_connect = self.checkbox_auto_connect.isChecked()
            else:
                auto_connect = POSTGRESQL_AUTO_CONNECT
        else:
            auto_connect = False

        self.hide()
        if auto_connect:
            from main.utils.connection_bdd.verification import VerificationWindow
            self.main_window = VerificationWindow(db_type=self.db_type)
        else:
            from main.page.page_3_login.login import LoginWindow
            self.main_window = LoginWindow(db_type=self.db_type)

        self.main_window.show()
        fade_widget(self.main_window, duration=300, fade_in=True)

    def afficher_message(self, message):
        self.message_label.setText(message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConfigurationWindow(db_type="PostgreSQL")
    window.show()
    sys.exit(app.exec())
