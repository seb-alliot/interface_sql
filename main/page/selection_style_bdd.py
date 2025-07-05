from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton
import subprocess
from settings import VERSION, APP_NAME
from main.utils.regles_visuelles.fad_widjet import fade_widget
from main.utils.fonction_diverse.recharge_env import recharger_env
from main.utils import fermer_et_transfere, Close
from main.utils.fonction_diverse import importer_module_bdd
from main.utils.fonction_diverse.mise_a_jour import VerifMajThread


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

        # Label unique pour afficher messages d'état (mise à jour, erreurs, etc)
        self.label_maj = QLabel("Initialisation...")
        self.label_maj.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_maj.setStyleSheet("color: white; font-size: 14px; padding: 10px;")
        layout.addWidget(self.label_maj)

        self.label = self._create_label("Sélectionnez la base de donnée :")
        layout.addWidget(self.label)

        self.combo = QComboBox()
        self.combo.addItems(["PostgreSQL", "MariaDB", "MongoDB", "SQLite"])
        self.combo.setMinimumSize(200, 30)
        self.combo.setMaximumSize(300, 45)
        layout.addWidget(self.combo)

        self.button = self._create_button("Continuer", self.tester_connection)
        layout.addWidget(self.button)

        self.setLayout(layout)

        # Lancer la vérification mise à jour dans un thread (une seule fois)
        self.thread_maj = VerifMajThread()
        self.thread_maj.maj_result.connect(self.update_label_maj)
        self.thread_maj.maj_finie.connect(self.lancer_nouvelle_version)
        self.thread_maj.start()

    def update_label_maj(self, message, color):
        self.label_maj.setText(message)
        self.label_maj.setStyleSheet(f"color: {color}; font-size: 14px; padding: 10px;")
        self.label_maj.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def lancer_nouvelle_version(self):
        chemin_nouvelle_version = "appli_by_itsuki.exe"
        try:
            subprocess.Popen([chemin_nouvelle_version])
        except Exception as e:
            self.update_label_maj(f"Erreur lancement nouvelle version : {e}", "red")
            return
        self.close()

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

    def tester_connection(self):
        recharger_env()
        choix = self.combo.currentText()

        if choix == "SQLite":
            self.update_label_maj("SQLite n'est pas encore pris en charge.", "red")
            return

        try:
            self.module = importer_module_bdd(choix)
            if not self.module:
                self.update_label_maj("Module introuvable pour ce type de base.", "red")
                return

            config_bdd = self.module.config()
            auto_connect = self.module.auto_connect()
            connection = self.module.connect(config_bdd)

            if connection and auto_connect:
                self.update_label_maj(f"Connexion réussie à {choix} !", "green")
                self.connection = connection
                from main.page.menu_principal_bdd import Menu_Principal_Window
                self.ouvrir_fenetre(Menu_Principal_Window)

            elif connection and not auto_connect:
                self.update_label_maj("Veuillez entrer vos identifiants de connexion :", "orange")
                self.connection = connection
                from main.page.login import LoginWindow
                self.ouvrir_fenetre(LoginWindow)

            else:
                self.update_label_maj("Mauvaise configuration veuillez la corriger :", "orange")
                from main.page.configuration import ConfigurationWindow
                self.ouvrir_fenetre(ConfigurationWindow)

        except Exception as e:
            self.update_label_maj(f"Erreur lors de la connexion : {e}", "red")

    def ouvrir_fenetre(self, fenetre_a_ouvrir):
        style_base_donne = self.combo.currentText()
        self.next_window = fenetre_a_ouvrir(style_base_donne, self.connection)
        self.next_window.show()
        fade_widget(self.next_window, duration=500, fade_in=True)
        fermer_et_transfere(self)

    def closeEvent(self, event):
        Close(self, event)
