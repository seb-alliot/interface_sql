import sys
from pathlib import Path
from dotenv import load_dotenv
project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))
# --- Fin de la correction ---
from main.utils.module.maria_db import connect_to_maria_database, MARIA_DB_CONFIG, MARIA_AUTO_CONNECT
from main.utils.module.postgres import connect_to_postgresql_database, POSTGRESQL_CONFIG, POSTGRESQL_AUTO_CONNECT
from main import center_on_screen
from main.utils.regles_visuelles.fad_widjet import fade_widget
from main.page.menu_principal_bdd import Menu_Principal_Window
from main.utils.fonction_diverse.recharge_env import recharger_env
from main.utils import Close


from settings import (
    APP_NAME,
    VERSION,
)
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
)
from PyQt6.QtCore import Qt



class LoginWindow(QWidget):
    def __init__(self, style_base_donné):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} - {VERSION}")
        self.resize(600, 400)
        center_on_screen(self)
        main_vertical_layout = QVBoxLayout()
        main_vertical_layout.addStretch(1)
        self.style_base_donné = style_base_donné
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
        recharger_env
        nom = self.input_pseudo.text().strip()
        if not nom:
            self.message_info.setText("Veuillez entrer un identifiant.")
            return
        password = self.input_password.text().strip()
        if not password:
            self.message_info.setText("Veuillez entrer un mot de passe.")
            return

        if self.style_base_donné == "PostgreSQL":

            identifiant = POSTGRESQL_CONFIG(user=nom, password=password)
            connection, error = connect_to_postgresql_database(identifiant)
            auto_connect = POSTGRESQL_AUTO_CONNECT
        elif self.style_base_donné == "MariaDB":
            auto_connect = MARIA_AUTO_CONNECT
            identifiant = MARIA_DB_CONFIG(user=nom, password=password)
            connection, error = connect_to_maria_database(identifiant)
        try:
            if connection and auto_connect is True:
                self.message_info.setText("Connexion réussie !")
                connection.close()
                fade_widget(self, duration=300, fade_in=False, finished_callback=lambda: self.show_main_window(nom))
            elif connection and auto_connect is False:
                self.message_info.setText("Veuillez entrer vos identifiants de connexion.")
                fade_widget(self, duration=300, fade_in=False, finished_callback=lambda: self.show_main_window())
            elif not connection:
                if error:
                    self.message_info.setText(f"Échec de la connexion : {error}")
                else:
                    self.message_info.setText("Échec de la connexion, veuillez vérifier vos identifiants.")

        except Exception as e:
            self.message_info.setText(f"Erreur lors de la connexion : {e}")

    def show_main_window(self):
        self.close()
        self.main_window = Menu_Principal_Window(self.style_base_donné)
        fade_widget(self.main_window, duration=300, fade_in=True)
        self.main_window.show()


    def closeEvent(self, event):
        Close(self, event)
