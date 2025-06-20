from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton
from PyQt6.QtCore import Qt
from main.page.menu import MenuWindow
from main.utils.gestion_bdd.connection_db import connect_to_postgresql_database, connect_to_maria_database
from main.page.configuration import ConfigurationWindow
from main.page.login import LoginWindow
from settings import POSTGRESQL_CONFIG, MARIA_DB_CONFIG, POSTGRESQL_AUTO_CONNECT, MARIA_AUTO_CONNECT,VERSION, APP_NAME
from main.utils.fonction_diverse.recharge_env import recharger_env

from main.utils.regles_visuelles.fad_widjet import fade_widget

class ChoixBDDWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} - {VERSION}")
        self.resize(600, 400)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = QLabel("Sélectionnez la base de donnée :")
        self.label.setMinimumWidth(200)
        self.label.setMaximumWidth(300)
        self.label.setMinimumHeight(30)
        self.label.setMaximumHeight(45)
        self.label.setStyleSheet("font-size: 14px; padding: 5px;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.combo = QComboBox()
        self.combo.addItems(["PostgreSQL", "MariaDB", "SQLite"])
        layout.addWidget(self.combo)

        self.button = QPushButton("Continuer")
        self.button.setMinimumWidth(200)
        self.button.setMaximumWidth(300)
        self.button.setMinimumHeight(30)
        self.button.setMaximumHeight(45)
        self.button.setStyleSheet("font-size: 14px; padding: 5px;")
        self.button.clicked.connect(self.tester_connection)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def tester_connection(self):
        recharger_env()
        choix = self.combo.currentText()
        connection = None

        if choix == "PostgreSQL":
            db_config = POSTGRESQL_CONFIG()
            auto_connect = POSTGRESQL_AUTO_CONNECT
            if auto_connect:
                connection, error = connect_to_postgresql_database(db_config)
                self._set_label("Connexion réussie!", "green")
                connection.close()
                fenetre_cible = MenuWindow
                self.ouvrir_fenetre(fenetre_cible)
            else:
                self._set_label("Veuillez entrer vos identifiants de connexion :", "orange")
                fenetre_cible = LoginWindow
                self.ouvrir_fenetre(fenetre_cible)

        elif choix == "MariaDB":
            db_config = MARIA_DB_CONFIG()
            auto_connect = MARIA_AUTO_CONNECT
            if auto_connect:
                connection, error = connect_to_maria_database(db_config)
                self._set_label("Connexion réussie!", "green")
                connection.close()
                fenetre_cible = MenuWindow
                self.ouvrir_fenetre(fenetre_cible)
            else:
                self._set_label("Veuillez entrer vos identifiants de connexion :", "orange")
                fenetre_cible = LoginWindow
                self.ouvrir_fenetre(fenetre_cible)

        elif choix == "SQLite":
            self._set_label("SQLite n'est pas encore implémenté.", "red")
            fade_widget(self, duration=500, fade_in=False,finished_callback=lambda: self.ouvrir_fenetre(ConfigurationWindow))
            return

        else:
            self._set_label(f"Connexion échouée : {error}", "red")
            fenetre_cible =ConfigurationWindow
            fade_widget(self, duration=500, fade_in=False,
                        finished_callback=lambda: self.ouvrir_fenetre(fenetre_cible))

    def _set_label(self, text, color):
        self.label.setText(text)
        self.label.setStyleSheet(f"font-size: 14px; color: {color};")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def ouvrir_fenetre(self, fenetre_a_ouvrir):
        self.close()
        choix = self.combo.currentText()
        self.verification_window = fenetre_a_ouvrir(db_type=choix)
        fade_widget(self.verification_window, duration=500, fade_in=True)
        self.verification_window.show()
