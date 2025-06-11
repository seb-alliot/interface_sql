import sys
from pathlib import Path
from settings import APP_NAME, VERSION

sys.path.append(str(Path(__file__).resolve().parent / "main"))

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
)
from PyQt6.QtCore import Qt

from main.utils.regle_visuel.fad_widjet import fade_widget
from main.utils.save_donne.config_bdd import save_bdd_config

from main import center_on_screen

class ConfigurationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} - v{VERSION}")
        self.resize(600, 400)
        center_on_screen(self)
        self.setFocus()

        self.inputs = {}

        # Layouts
        main_vertical_layout = QVBoxLayout()
        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Titre principal
        self.title_label = QLabel("Configuration de la base de donnée.")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        content_layout.addWidget(self.title_label)

        # Message dynamique
        self.message_label = QLabel("")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setStyleSheet("font-size: 14px; color: orange;")
        content_layout.addWidget(self.message_label)

        # Champs de saisie
        champs = [
            ("bdd_name", "Entrez le nom de la base de données", QLineEdit.EchoMode.Normal),
            ("user", "Entrez le nom d'utilisateur", QLineEdit.EchoMode.Normal),
            ("password", "Entrez le mot de passe", QLineEdit.EchoMode.Password),
            ("host", "Entrez l'hôte de la base de données", QLineEdit.EchoMode.Normal),
            ("port", "Entrez le port de la base de données", QLineEdit.EchoMode.Normal),
        ]

        for nom_input, placeholder, echo in champs:
            champ = self.creer_input(placeholder, echo)
            self.inputs[nom_input] = champ
            content_layout.addWidget(champ, alignment=Qt.AlignmentFlag.AlignCenter)

        # Bouton de validation
        self.validation_button = QPushButton("Valider la configuration")
        self.validation_button.setMinimumSize(200, 30)
        self.validation_button.setMaximumSize(300, 30)
        self.validation_button.clicked.connect(self.bouton_validation)
        content_layout.addWidget(self.validation_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Organisation finale
        main_vertical_layout.addStretch(1)
        main_vertical_layout.addLayout(content_layout)
        main_vertical_layout.addStretch(1)
        self.setLayout(main_vertical_layout)

    def creer_input(self, placeholder, echo_mode):
        champ = QLineEdit()
        champ.setMinimumSize(200, 30)
        champ.setMaximumSize(300, 30)
        champ.setEchoMode(echo_mode)
        champ.setPlaceholderText(placeholder)
        champ.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return champ

    def bouton_validation(self):
        dbname = self.inputs["bdd_name"].text().strip()
        user = self.inputs["user"].text().strip()
        password = self.inputs["password"].text().strip()
        host = self.inputs["host"].text().strip()
        port_text = self.inputs["port"].text().strip()

        if not (dbname and user and password and host and port_text):
            self.afficher_message("Veuillez remplir tous les champs.")
            return

        try:
            port = int(port_text)
            if not (1 <= port <= 65535):
                raise ValueError
        except ValueError:
            self.afficher_message("Le port doit être un nombre entre 1 et 65535.")
            return

        db_config = {
            "DB_NAME": dbname,
            "DB_USER": user,
            "DB_PASSWORD": password,
            "DB_HOST": host,
            "DB_PORT": port,
        }

        try:
            save_bdd_config(db_config)
            self.afficher_message("Configuration enregistrée avec succès !")
            fade_widget(self, duration=1500, fade_in=False, finished_callback=self.on_fade_out_finished)
        except FileNotFoundError as e:
            self.afficher_message(str(e))
        except Exception as e:
            self.afficher_message(f"Erreur lors de l'enregistrement : {e}")

    def on_fade_out_finished(self):
        self.close()
        from main.page.page_1_verification import VerificationWindow
        self.restart_window = VerificationWindow()
        fade_widget(self.restart_window, duration=300, fade_in=True)
        self.restart_window.show()

    def afficher_message(self, message):
        self.message_label.setText(message)
