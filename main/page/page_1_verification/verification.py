from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt , QTimer

from main.page.page_1_verification.connection_db import connect_to_database
from main import center_on_screen
from main.utils.regles_visuelles.fad_widjet import fade_widget
from main.page.page_2_configuration.configuration import ConfigurationWindow
from main.page.page_3_connection.connection import LoginWindow
from settings import APP_NAME, VERSION, MAJ_DB_CONFIG
from dotenv import load_dotenv


class VerificationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} - v{VERSION}")
        self.resize(600, 400)
        center_on_screen(self)

        layout = QVBoxLayout()
        self.label_info = QLabel("Vérification de la connexion...")
        self.label_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_info)
        self.setLayout(layout)

        # Lancer la vérification après un petit délai pour laisser le temps à l'affichage
        QTimer.singleShot(100, self.verifier_et_ouvrir)

    def verifier_et_ouvrir(self):
        load_dotenv(override=True)
        DB_CONFIG = MAJ_DB_CONFIG()
        connection, erreur = connect_to_database(DB_CONFIG)
        if connection:
            self.label_info.setText("Connexion réussie !")
            fade_widget(self, duration=500, fade_in=False, finished_callback=self.afficher_login_window)
        else:
            self.label_info.setText("Connexion échouée, veuillez configurer la base.")
            fade_widget(self, duration=500, fade_in=False, finished_callback=self.afficher_configuration_window)

    def afficher_login_window(self):
        # Cacher cette fenêtre sans la fermer brutalement
        self.hide()
        self.main_window = LoginWindow(f"{APP_NAME} - v{VERSION}")
        self.main_window.show()
        fade_widget(self.main_window, duration=500, fade_in=True)
        # Détruire l'ancienne fenêtre après un court délai
        QTimer.singleShot(1000, self.deleteLater)

    def afficher_configuration_window(self):
        self.hide()
        self.config_window = ConfigurationWindow()
        self.config_window.show()
        fade_widget(self.config_window, duration=500, fade_in=True)
        QTimer.singleShot(1000, self.deleteLater)
