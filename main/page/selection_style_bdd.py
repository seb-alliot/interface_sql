from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton

from settings import VERSION, APP_NAME
from main.utils.regles_visuelles.fad_widjet import fade_widget
from main.utils.fonction_diverse.recharge_env import recharger_env
from main.utils import fermer_et_transfere, Close
from main.utils.fonction_diverse import importer_module_bdd
import psutil
import sys


if "--from-launcher" not in sys.argv:
    from PyQt6.QtWidgets import QApplication, QMessageBox
    app = QApplication(sys.argv)
    QMessageBox.critical(None, "Erreur", "L'application doit être lancée via le launcher.")
    sys.exit(1)


class ChoixBDDWindow(QWidget):
    def __init__(self, connection=None, style_base_donne=None):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} - {VERSION}")
        self.resize(600, 400)
        self.style_base_donne = style_base_donne
        self.connection = connection
        self.module = None

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = self._create_label("Sélectionnez la base de donnée :")
        layout.addWidget(self.label)

        self.combo = QComboBox()
        self.combo.addItems(["PostgreSQL", "MariaDB", "MongoDB", "SQLite"])
        self.combo.setMinimumSize(200, 30)
        self.combo.setMaximumSize(300, 45)
        layout.addWidget(self.combo)

        self.label_connexion = self._create_label("")
        layout.addWidget(self.label_connexion)

        self.button = self._create_button("Continuer", self.tester_connection)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def _create_label(self, text):
        label = QLabel(text)
        label.setMaximumSize(300, 45)
        label.setStyleSheet("font-size: 14px; padding: 5px;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label

    def _create_button(self, text, callback):
        button = QPushButton(text)
        button.setMinimumSize(200, 30)
        button.setMaximumSize(300, 45)
        button.setStyleSheet("font-size: 14px; padding: 5px;")
        button.clicked.connect(callback)
        return button

    def update_connexion_label(self, message, color):
        self.label_connexion.setText(message)
        self.label_connexion.setStyleSheet(f"color: {color}; font-size: 14px; padding: 10px;")
        self.label_connexion.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def tester_connection(self):
        recharger_env()
        choix = self.combo.currentText()

        if choix == "SQLite":
            self.update_connexion_label("SQLite n'est pas encore pris en charge.", "red")
            return

        try:
            self.module = importer_module_bdd(choix)
            if not self.module:
                self.update_connexion_label("Module introuvable pour ce type de base.", "red")
                return

            config_bdd = self.module.config()
            auto_connect = self.module.auto_connect()
            connection = self.module.connect(config_bdd)

            if connection and auto_connect:
                self.update_connexion_label(f"Connexion réussie à {choix} !", "green")
                self.connection = connection
                from main.page.menu_principal_bdd import Menu_Principal_Window
                self.ouvrir_fenetre(Menu_Principal_Window)

            elif connection and not auto_connect:
                self.update_connexion_label("Veuillez entrer vos identifiants de connexion :", "orange")
                self.connection = connection
                from main.page.login import LoginWindow
                self.ouvrir_fenetre(LoginWindow)

            else:
                self.update_connexion_label("Mauvaise configuration veuillez la corriger :", "orange")
                from main.page.configuration import ConfigurationWindow
                self.ouvrir_fenetre(ConfigurationWindow)

        except Exception as e:
            self.update_connexion_label(f"Erreur lors de la connexion : {e}", "red")

    def ouvrir_fenetre(self, fenetre_a_ouvrir):
        style_base_donne = self.combo.currentText()
        self.next_window = fenetre_a_ouvrir(style_base_donne, self.connection)
        self.next_window.show()
        fade_widget(self.next_window, duration=500, fade_in=True)
        fermer_et_transfere(self)

    def closeEvent(self, event):
        Close(self, event)
