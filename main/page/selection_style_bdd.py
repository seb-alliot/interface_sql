from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton
from PyQt6.QtCore import Qt
from main.page.menu_principal_bdd import Menu_Principal_Window
from main.page.configuration import ConfigurationWindow
from main.page.login import LoginWindow
from main.utils.module.maria_db import connect_to_maria_database, MARIA_DB_CONFIG, MARIA_AUTO_CONNECT
from main.utils.module.postgres import connect_to_postgresql_database, POSTGRESQL_CONFIG, POSTGRESQL_AUTO_CONNECT
from main.utils.regles_visuelles.fad_widjet import fade_widget
from main.utils.fonction_diverse.recharge_env import recharger_env
from settings import VERSION, APP_NAME

# Dictionnaire factorisé pour les configs de base de données
db_configs = {
    "PostgreSQL": {
        "config_bdd": POSTGRESQL_CONFIG,
        "connector": connect_to_postgresql_database,
        "auto_connect": POSTGRESQL_AUTO_CONNECT,
    },
    "MariaDB": {
        "config_bdd": MARIA_DB_CONFIG,
        "connector": connect_to_maria_database,
        "auto_connect": MARIA_AUTO_CONNECT
    }
}

class ChoixBDDWindow(QWidget):
    def __init__(self, style_base_donné=None):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} - {VERSION}")
        self.resize(600, 400)
        self.style_base_donné = style_base_donné

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label = self._create_label("Sélectionnez la base de donnée :")
        layout.addWidget(self.label)

        self.combo = QComboBox()
        self.combo.addItems(["PostgreSQL", "MariaDB", "SQLite"])
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

        if choix in db_configs:
            config_bdd = db_configs[choix]["config_bdd"]
            auto_connect = db_configs[choix]["auto_connect"]
            connect_bdd = db_configs[choix]["connector"]

            db_config = config_bdd()

            if auto_connect:
                connection, error = connect_bdd(db_config)
                if connection:
                    self._set_label("Connexion réussie!", "green")
                    connection.close()
                    self.ouvrir_fenetre(Menu_Principal_Window)
                else:
                    self._set_label(f"Connexion échouée : {error}", "red")
                    self._fade_to(ConfigurationWindow)
            else:
                self._set_label("Veuillez entrer vos identifiants de connexion :", "orange")
                self.ouvrir_fenetre(LoginWindow)

        elif choix == "SQLite":
            self._set_label("SQLite n'est pas encore implémenté.", "red")
        else:
            self._set_label("Type de base de donnée non reconnu.", "red")

    def _set_label(self, text, color):
        self.label.setText(text)
        self.label.setStyleSheet(f"font-size: 14px; color: {color};")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def ouvrir_fenetre(self, fenetre_a_ouvrir):
        self.close()
        style_base_donné = self.combo.currentText()
        self.next_window = fenetre_a_ouvrir(style_base_donné)
        print("_" * 40)
        print(f"ChoixBDDWindow")
        print(f"style_base_donné selection du langue de la base, postgres, maria etc : {style_base_donné}")
        fade_widget(self.next_window, duration=500, fade_in=True)
        self.next_window.show()

    def _fade_to(self, fenetre_a_ouvrir):
        fade_widget(self, duration=500, fade_in=False,
                    finished_callback=lambda: self.ouvrir_fenetre(fenetre_a_ouvrir))
