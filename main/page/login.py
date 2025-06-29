import sys
from pathlib import Path
import os

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from main import center_on_screen
from main.utils.regles_visuelles.fad_widjet import fade_widget
from main.page.menu_principal_bdd import Menu_Principal_Window
from main.utils.fonction_diverse.recharge_env import recharger_env
from main.utils import Close
from main.utils.fonction_diverse import importer_module_bdd

from settings import APP_NAME, VERSION
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt6.QtCore import Qt


class LoginWindow(QWidget):
    def __init__(self, style_base_donné):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} - {VERSION}")
        self.resize(600, 400)
        center_on_screen(self)
        self.style_base_donné = style_base_donné
        self.module = importer_module_bdd(self.style_base_donné)
        self.setFocus()

        main_vertical_layout = QVBoxLayout()
        main_vertical_layout.addStretch(1)

        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title_label = QLabel("Connection à la base de données")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        content_layout.addWidget(self.title_label)

        self.message_label = QLabel("")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setStyleSheet("font-size: 14px; color: orange;")
        content_layout.addWidget(self.message_label)

        self.input_pseudo = QLineEdit()
        self.input_pseudo.setMinimumSize(200, 30)
        self.input_pseudo.setMaximumSize(300, 30)
        self.input_pseudo.setEchoMode(QLineEdit.EchoMode.Normal)
        self.input_pseudo.setPlaceholderText("Entrez votre prénom")
        self.input_pseudo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(self.input_pseudo, alignment=Qt.AlignmentFlag.AlignCenter)

        self.input_password = QLineEdit()
        self.input_password.setMinimumSize(200, 30)
        self.input_password.setMaximumSize(300, 30)
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_password.setPlaceholderText("Votre mot de passe")
        self.input_password.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(self.input_password, alignment=Qt.AlignmentFlag.AlignCenter)

        self.bouton = QPushButton("Se connecter")
        self.bouton.setMinimumSize(200, 30)
        self.bouton.setMaximumSize(300, 30)
        self.bouton.clicked.connect(self.bouton_connection)
        content_layout.addWidget(self.bouton, alignment=Qt.AlignmentFlag.AlignCenter)

        self.message_info = QLabel("")
        self.message_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(self.message_info, alignment=Qt.AlignmentFlag.AlignCenter)

        main_vertical_layout.addLayout(content_layout)
        main_vertical_layout.addStretch(1)

        self.setLayout(main_vertical_layout)
        self.main_window = None

    def bouton_connection(self):
        recharger_env()
        nom = self.input_pseudo.text().strip()
        if not nom:
            self.message_info.setText("Veuillez entrer un identifiant.")
            return

        password = self.input_password.text().strip()
        if not password:
            self.message_info.setText("Veuillez entrer un mot de passe.")
            return

        try:
            config = self.module["config"].get_config(user=nom, password=password)
            connection = self.module["connection"].connect(config)

            # auto_connect doit venir du .env avec le bon prefixe
            auto_connect_var = f"{self.style_base_donné.upper()}_AUTO_CONNECT"
            auto_connect = os.getenv(auto_connect_var, "False").lower() == "true"

            if connection and auto_connect:
                self.message_info.setText("Connexion réussie !")
                connection.close()
                fade_widget(self, duration=300, fade_in=False, finished_callback=lambda: self.show_main_window(nom))
            elif connection and not auto_connect:
                self.message_info.setText("Veuillez entrer vos identifiants de connexion.")
                fade_widget(self, duration=300, fade_in=False, finished_callback=lambda: self.show_main_window())
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
