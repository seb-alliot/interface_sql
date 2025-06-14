import sys
from pathlib import Path
from settings import APP_NAME, VERSION, POSTGRESQL_AUTO_CONNECT, POSTGRES_DB, recharge_env

sys.path.append(str(Path(__file__).resolve().parent / "main"))

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QCheckBox, QApplication
)
from PyQt6.QtCore import Qt, QTimer

from main.utils.regles_visuelles.fad_widjet import fade_widget
from main.utils.save_donne.config_bdd import save_bdd_config
from main.page.page_2_menu.menu import MenuWindow
from dotenv import load_dotenv
load_dotenv()
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

        main_vertical_layout = QVBoxLayout()
        main_vertical_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title_label = QLabel(f"Configuration de la base de données {db_type}.")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: black;")
        main_vertical_layout.addWidget(self.title_label)

        self.message_label = QLabel("")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setStyleSheet("font-size: 14px; color: orange;")
        main_vertical_layout.addWidget(self.message_label)

        # Afficher checkbox auto connect uniquement pour PostgreSQL
        if db_type == "PostgreSQL":
            self.checkbox_auto_connect = QCheckBox("Connexion automatique")
            # Optionnel : coché par défaut si config existante et auto_connect à True
            if POSTGRESQL_AUTO_CONNECT:
                self.checkbox_auto_connect.setChecked(True)
            main_vertical_layout.addWidget(self.checkbox_auto_connect, alignment=Qt.AlignmentFlag.AlignCenter)

            # Pré-remplissage depuis POSTGRES_DB si existant
            if POSTGRES_DB.get("dbname", "default") == "default":
                champs = [
                    ("bdd_name", "Nom de la base de données", QLineEdit.EchoMode.Normal, ""),
                    ("user", "Nom d'utilisateur", QLineEdit.EchoMode.Normal, ""),
                    ("password", "Mot de passe", QLineEdit.EchoMode.Password, ""),
                    ("host", "Hôte de la base de données", QLineEdit.EchoMode.Normal, ""),
                    ("port", "Port de la base de données", QLineEdit.EchoMode.Normal, ""),
                ]
            else:
                champs = [
                    ("bdd_name", "Nom de la base de données", QLineEdit.EchoMode.Normal, POSTGRES_DB.get("dbname", "")),
                    ("user", "Nom d'utilisateur", QLineEdit.EchoMode.Normal, POSTGRES_DB.get("user", "")),
                    ("password", "Mot de passe", QLineEdit.EchoMode.Password, POSTGRES_DB.get("password", "")),
                    ("host", "Hôte de la base de données", QLineEdit.EchoMode.Normal, POSTGRES_DB.get("host", "")),
                    ("port", "Port de la base de données", QLineEdit.EchoMode.Normal, str(POSTGRES_DB.get("port", ""))),
                ]

            for nom_input, placeholder, echo, valeur_defaut in champs:
                champ = self.creer_input(placeholder, echo)
                if valeur_defaut:
                    champ.setText(valeur_defaut)
                self.inputs[nom_input] = champ
                main_vertical_layout.addWidget(champ, alignment=Qt.AlignmentFlag.AlignCenter)
        else:
            # Pour les autres types, tu peux reproduire un comportement similaire ici si besoin
            pass

        self.validation_button = QPushButton("Valider la configuration")
        self.validation_button.setFixedSize(200, 30)
        self.validation_button.clicked.connect(self.bouton_validation)
        main_vertical_layout.addWidget(self.validation_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.retour_button = QPushButton("Retour")
        self.retour_button.setFixedSize(200, 30)
        self.retour_button.clicked.connect(self.retour)
        main_vertical_layout.addWidget(self.retour_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_vertical_layout)

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
        dbname = self.inputs["bdd_name"].text().strip()
        user = self.inputs["user"].text().strip()
        password = self.inputs["password"].text().strip()
        host = self.inputs["host"].text().strip()
        port = self.inputs["port"].text().strip()

        if not (dbname and user and password and host and port):
            self.afficher_message("Veuillez remplir tous les champs.")
            return

        try:
            port = int(port)
            if not (1 <= port <= 65535):
                raise ValueError
        except ValueError:
            self.afficher_message("Le port doit être un nombre entre 1 et 65535.")
            return

        auto_connect = False
        if hasattr(self, "checkbox_auto_connect"):
            auto_connect = self.checkbox_auto_connect.isChecked()

        if self.db_type == "PostgreSQL":
            db_config = {
                "POSTGRESQL_NAME": dbname,
                "POSTGRESQL_USER": user,
                "POSTGRESQL_PASSWORD": password,
                "POSTGRESQL_HOST": host,
                "POSTGRESQL_PORT": port,
                "POSTGRESQL_AUTO_CONNECT": auto_connect,
            }
        else:
            db_config = {
                "DB_NAME": dbname,
                "DB_USER": user,
                "DB_PASSWORD": password,
                "DB_HOST": host,
                "DB_PORT": port,
                "DB_AUTO_CONNECT": auto_connect,
            }

        try:
            save_bdd_config(db_config)
            self.afficher_message("Configuration enregistrée avec succès !")
            recharge_env()  # Recharge les variables d'environnement
            if auto_connect:
                self.hide()
                self.main_window = MenuWindow(db_type=self.db_type)
                self.main_window.show()
                fade_widget(self.main_window, duration=300, fade_in=True)
            else:
                self.afficher_message("Configuration enregistrée. Veuillez vous connecter manuellement.")
        except Exception as e:
            self.afficher_message(f"Erreur lors de l'enregistrement : {e}")

    def afficher_message(self, message):
        self.message_label.setText(message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConfigurationWindow()  # attention à passer db_type !
    window.show()
    sys.exit(app.exec())
