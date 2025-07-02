from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton
from PyQt6.QtCore import Qt
from main.page.menu_principal_bdd import Menu_Principal_Window
from main.page.configuration import ConfigurationWindow
from main.page.login import LoginWindow

from main.utils.regles_visuelles.fad_widjet import fade_widget
from main.utils.fonction_diverse.recharge_env import recharger_env
from settings import VERSION, APP_NAME
from main.utils import fermer_et_transfere
from main.utils.fonction_diverse import importer_module_bdd


class ChoixBDDWindow(QWidget):
    def __init__(self, connection=None, style_base_donne=None):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} - {VERSION}")
        self.resize(600, 400)
        self.style_base_donne = style_base_donne
        self.connection = connection
        self.module = None  # stockera l'instance ModuleBDD

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = self._create_label("Sélectionnez la base de donnée :")
        layout.addWidget(self.label)

        self.combo = QComboBox()
        self.combo.addItems(["PostgreSQL", "MariaDB", "MongoDB", "SQLite"])
        layout.addWidget(self.combo)

        self.button = self._create_button("Continuer", self.tester_connection)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def _create_label(self, text):
        label = QLabel(text)
        label.setFixedSize(300, 45)
        label.setStyleSheet("font-size: 14px; padding: 5px;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label

    def _create_button(self, text, callback):
        button = QPushButton(text)
        button.setFixedSize(300, 45)
        button.setStyleSheet("font-size: 14px; padding: 5px;")
        button.clicked.connect(callback)
        return button

    def tester_connection(self):
        recharger_env()
        choix = self.combo.currentText()

        if choix == "SQLite":
            self._set_label("SQLite n'est pas encore pris en charge.", "red")
            return

        try:
            # Import dynamique du module BDD (config + connection)
            self.module = importer_module_bdd(choix)
            if not self.module:
                self._set_label("Module introuvable pour ce type de base.", "red")
                return

            # Récupérer la config (avec config() sans argument ici)
            config_bdd = self.module.config()

            # Auto connect si possible (booléen)
            auto_connect = self.module.auto_connect()

            if auto_connect:
                # Connection retourne juste l'objet connexion ou None
                connection = self.module.connect(config_bdd)
                if connection and auto_connect:
                    self._set_label(f"Connexion réussie à {choix} !", "green")
                    self.connection = connection
                    # Ouvre la fenêtre principale en passant style et connexion
                    self.ouvrir_fenetre(Menu_Principal_Window)
                elif connection and not auto_connect:
                    self._set_label("Veuillez entrer vos identifiants de connexion :", "orange")
                    # Ouvre la fenêtre de login, qui doit gérer la connexion manuelle
                    self.ouvrir_fenetre(LoginWindow)
            else:
                self._set_label("Mauvaise configuration veuillez la corriger :", "orange")
                # Ouvre la fenêtre de login, qui doit gérer la connexion manuelle
                self.ouvrir_fenetre(ConfigurationWindow)

        except Exception as e:
            self._set_label(f"Erreur lors de la connexion : {e}", "red")

    def _set_label(self, text, color):
        self.label.setText(text)
        self.label.setStyleSheet(f"font-size: 14px; color: {color};")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def ouvrir_fenetre(self, fenetre_a_ouvrir):
        style_base_donne = self.combo.currentText()
        self.next_window = fenetre_a_ouvrir(
            style_base_donne,
            self.connection,
        )
        self.next_window.show()
        fade_widget(self.next_window, duration=500, fade_in=True)
        fermer_et_transfere(self)
