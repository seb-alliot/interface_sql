import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))
# --- Fin de la correction ---

from main.page.page_1_verification.code.connection_db import connect_to_database
from main import center_on_screen
from main.utils.regle_visuel.fad_widjet import fade_widget
from main.utils.regle_visuel.transition_connection import TransitionWindow
from main.page.page_2_configuration.configuration import ConfigurationWindow
from main.page.page_3_connection.connection import LoginWindow

from settings import APP_NAME, VERSION, DB_CONFIG
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QScreen


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

        # On lance la vérification à la création (ou peut-être via un bouton)
        self.verifier_et_ouvrir()

    def verifier_connexion(self):
        connection, erreur = connect_to_database(DB_CONFIG)
        if connection:
            print(f"les paramètres de connexion sont : {DB_CONFIG}")
            return True
        else:
            return False


    def verifier_et_ouvrir(self):
        connection, erreur = connect_to_database(DB_CONFIG)
        if connection:
            self.label_info.setText("Connexion à la base de donnée réussie !")
            fade_widget(self, duration=300, fade_in=False, finished_callback=self.ouvrir_fenetre_principale)
        else:
            self.label_info.setText("Connexion échouée, veuillez configurer la base.")
            fade_widget(self, duration=300, fade_in=False, finished_callback=self.ouvrir_fenetre_configuration)

    def ouvrir_fenetre_principale(self):
        self.close()
        self.main_window = LoginWindow(f"{APP_NAME} - v{VERSION}")
        fade_widget(self.main_window, duration=300, fade_in=True)
        self.main_window.show()

    def ouvrir_fenetre_configuration(self):
        self.close()
        self.config_window = ConfigurationWindow(f"{APP_NAME} - v{VERSION}")
        fade_widget(self.config_window, duration=300, fade_in=True)
        self.config_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = VerificationWindow()
    fenetre.show()
    sys.exit(app.exec())