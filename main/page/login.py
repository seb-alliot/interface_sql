import sys
from pathlib import Path
import os

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from main import center_on_screen
from main.utils.regles_visuelles.fad_widjet import fade_widget
from main.page.menu_principal_bdd import Menu_Principal_Window
from main.page.configuration import ConfigurationWindow
from main.utils.fonction_diverse.recharge_env import recharger_env
from main.utils import Close
from main.utils.fonction_diverse import importer_module_bdd
from main.utils import fermer_et_transfere


from settings import APP_NAME, VERSION
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt6.QtCore import Qt


class LoginWindow(QWidget):
    def __init__(self, style_base_donne, connection):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} - {VERSION}")
        self.resize(600, 400)
        center_on_screen(self)
        self.style_base_donne = style_base_donne
        self.connection = connection
        self.module = importer_module_bdd(self.style_base_donne)
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

        self.bouton_config = QPushButton("Configurer la base de données")
        self.bouton_config.setMinimumSize(200, 30)
        self.bouton_config.setMaximumSize(300, 30)
        self.bouton_config.clicked.connect(self.show_main_config)
        content_layout.addWidget(self.bouton_config, alignment=Qt.AlignmentFlag.AlignCenter)

        self.message_info = QLabel("")
        self.message_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(self.message_info, alignment=Qt.AlignmentFlag.AlignCenter)

        main_vertical_layout.addLayout(content_layout)
        main_vertical_layout.addStretch(1)

        self.setLayout(main_vertical_layout)
        self.main_window = None

    def bouton_connection(self):
        recharger_env()
        user = self.input_pseudo.text().strip()
        password = self.input_password.text().strip()

        if not user:
            self.message_info.setText("Veuillez entrer un identifiant.")
            return
        if not password:
            self.message_info.setText("Veuillez entrer un mot de passe.")
            return

        try:
            config = self.module.config(user=user, password=password)

            if config is None:
                self.message_info.setText("Configuration invalide.")
                return

            connection, erreur = self.module.connect(config)

            if connection:
                self.message_info.setText("Connexion réussie !")
                self.connection = connection
                fade_widget(self, duration=300, fade_in=False, finished_callback=self.show_main_window)
            else:
                self.message_info.setText(f"Identifiant ou mot de passe incorrect : {erreur}")
                return


        except Exception as e:
            self.message_info.setText(f"Erreur : {e}")

    def show_main_config(self):
        fermer_et_transfere(self)
        self.config_window = ConfigurationWindow(
            self.style_base_donne,
            connection=self.connection,
        )
        fade_widget(self.config_window, duration=300, fade_in=True)
        self.config_window.show()
    def show_main_window(self):
        fermer_et_transfere(self)
        self.main_window = Menu_Principal_Window(
            self.style_base_donne,
            connection=self.connection,
            choix_bdd=None
            )
        fade_widget(self.main_window, duration=300, fade_in=True)
        self.main_window.show()

    def closeEvent(self, event):
        Close(self, event)
