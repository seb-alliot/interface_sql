import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))
# --- Fin de la correction ---

from main.page.page_1_verification.connection_db import connect_to_database
from main import center_on_screen
from main.utils.regles_visuelles.fad_widjet import fade_widget
from main.utils.regles_visuelles.transition_connection import TransitionWindow
from main.page.page_2_configuration.configuration import ConfigurationWindow
from main.page.page_4_menu.menu import MenuWindow


from settings import APP_NAME, VERSION, DB_CONFIG
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QScreen



# --- Classe MainWindow ---
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interface perso sql")
        self.resize(600, 400)
        center_on_screen(self)

        layout = QVBoxLayout()

        self.welcome_label = QLabel(f"Vous êtes sur la page de login.")
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.welcome_label)

        self.setLayout(layout)

class LoginWindow(QWidget):
    def __init__(self, nom):
        super().__init__()
        self.nom = nom
        self.setWindowTitle(f"{APP_NAME} - v{VERSION}")
        self.resize(600, 400)
        center_on_screen(self)
        main_vertical_layout = QVBoxLayout()
        main_vertical_layout.addStretch(1)
        self.setFocus()

        # Sous-layout pour les éléments de connexion (inputs, bouton, message)
        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter) # Centre horizontalement les widgets dans ce layout

        # Titre principal
        self.title_label = QLabel("Connection à la base de données")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        content_layout.addWidget(self.title_label)

        # Message dynamique
        self.message_label = QLabel("")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setStyleSheet("font-size: 14px; color: orange;")
        content_layout.addWidget(self.message_label)

        self.input_pseudo = QLineEdit()
        self.input_pseudo.setMinimumSize(200, 30)
        self.input_pseudo.setMaximumSize(300, 30)
        self.input_pseudo.setEchoMode(QLineEdit.EchoMode.Normal)  # Normal pour le pseudo
        self.input_pseudo.setPlaceholderText("Entrez votre prénom")
        self.input_pseudo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Ajout de l'alignement pour le widget au sein du layout
        content_layout.addWidget(self.input_pseudo, alignment=Qt.AlignmentFlag.AlignCenter)

        self.input_password = QLineEdit()
        self.input_password.setMinimumSize(200, 30)
        self.input_password.setMaximumSize(300, 30)
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_password.setPlaceholderText("Votre mot de passe")
        self.input_password.setAlignment(Qt.AlignmentFlag.AlignCenter)  # <-- Ceci centre le texte et le placeholder
        content_layout.addWidget(self.input_password, alignment=Qt.AlignmentFlag.AlignCenter)

        self.bouton = QPushButton("Se connecter")
        self.bouton.setMinimumSize(200, 30)
        self.bouton.setMaximumSize(300, 30)
        self.bouton.clicked.connect(self.bouton_connection)
        # Ajout de l'alignement pour le widget au sein du layout
        content_layout.addWidget(self.bouton, alignment=Qt.AlignmentFlag.AlignCenter)

        self.message_info = QLabel("")
        self.message_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # L'alignement du QLabel est déjà fait sur son texte,
        # mais on peut aussi spécifier l'alignement du widget lui-même dans le layout.
        content_layout.addWidget(self.message_info, alignment=Qt.AlignmentFlag.AlignCenter)

        # Ajoute le sous-layout de contenu au layout vertical principal
        main_vertical_layout.addLayout(content_layout)
        main_vertical_layout.addStretch(1) # Pousse le contenu vers le haut

        self.setLayout(main_vertical_layout) # Le layout principal de la fenêtre est maintenant main_vertical_layout

        self.main_window = None

    def bouton_connection(self):
        nom = self.input_pseudo.text().strip()
        if not nom:
            self.message_info.setText("Veuillez entrer un identifiant.")
            return
        password = self.input_password.text().strip()
        if not password:
            self.message_info.setText("Veuillez entrer un mot de passe.")
            return

        if nom == DB_CONFIG['user'] and password == DB_CONFIG['password']:
            try:
                connection, error = connect_to_database()
                if connection:
                    connection.close()
                    # Lancement du fade sur la fenêtre entière
                    fade_widget(self, duration=300, fade_in=False, finished_callback=lambda: self.on_fade_out_finished(nom))
                else:
                    self.message_info.setText("Échec de la connexion à la base de données.")
            except Exception as e:
                self.message_info.setText(f"Identifiants incorrects ou erreur : {e}")
        else:
            self.message_info.setText("Identifiants incorrects.")

    def on_fade_out_finished(self, nom):
        self.close()
        self.transition_window = TransitionWindow(nom, on_transition_done=lambda: self.start_main_window(nom))
        fade_widget(self.transition_window, duration=300, fade_in=True)
        self.transition_window.show()

    def start_main_window(self, nom):
        fade_widget(self.transition_window, duration=300, fade_in=False, finished_callback=lambda: self.show_main_window(nom))

    def show_main_window(self, nom):
        self.transition_window.close()
        self.main_window = MenuWindow(nom)
        fade_widget(self.main_window, duration=300, fade_in=True)
        self.main_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    from main.page.page_1_verification.verification import VerificationWindow

    fenetre = VerificationWindow()
    fenetre.show()

    sys.exit(app.exec())
