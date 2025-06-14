from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton
from PyQt6.QtCore import Qt
from main.utils.connection_bdd.verification import VerificationWindow
from main.page.page_2_menu.menu import MenuWindow
from main.utils.connection_bdd.connection_db import connect_to_sql_database
from main.page.configuration.configuration import ConfigurationWindow
from main.page.page_3_login.login import LoginWindow
import settings
from settings import POSTGRESQL_CONFIG


from main.utils.regles_visuelles.fad_widjet import fade_widget

class ChoixBDDWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Choix de la base de donnée")
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
        self.combo.addItems(["PostgreSQL", "SQLite"])
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
        choix = self.combo.currentText()
        if choix == "PostgreSQL":
            db_config = POSTGRESQL_CONFIG()
            auto_connect = settings.POSTGRESQL_AUTO_CONNECT
            connection, error = connect_to_sql_database(db_config)

            if connection and auto_connect is True:
                self._set_label("Connexion réussie!", "green")
                connection.close()
                fade_widget(self, duration=500, fade_in=False, finished_callback=self.lancer_menu)

            elif connection and auto_connect is False:
                self._set_label("Veuillez entrer vos identifiants de connexion :", "orange")
                fade_widget(self, duration=500, fade_in=False, finished_callback=self.lancer_login)
            elif not connection:
                self._set_label(f"Connexion échouée : {error}", "red")
                fade_widget(self, duration=500, fade_in=False, finished_callback=self.lancer_configuration)
            else:
                self._set_label(f"Connexion échouée : {error}", "red")
                self.button.setText("Réessayer")


    def _set_label(self, text, color):
        """Helper to streamline label modifications."""
        self.label.setText(text)
        self.label.setStyleSheet(f"font-size: 14px; color: {color};")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def lancer_login(self):
        choix = self.combo.currentText()
        self.close()
        self.verification_window = LoginWindow(db_type=choix)
        fade_widget(self.verification_window, duration=500, fade_in=True)
        self.verification_window.show()


    def lancer_menu(self):
        choix = self.combo.currentText()
        self.close()
        self.config_window = MenuWindow(db_type=choix)
        fade_widget(self.config_window, duration=500, fade_in=True)
        self.config_window.show()

    def lancer_configuration(self):
        choix = self.combo.currentText()
        self.close()
        self.verification_window = ConfigurationWindow(db_type=choix)
        fade_widget(self.verification_window, duration=500, fade_in=True)
        self.verification_window.show()
