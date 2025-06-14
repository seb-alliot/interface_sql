from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QApplication
from PyQt6.QtCore import Qt , QTimer

from main.utils.connection_bdd.connection_db import connect_to_sql_database
from main import center_on_screen
from main.utils.regles_visuelles.fad_widjet import fade_widget
from main.utils.save_donne.configuration import ConfigurationWindow

from settings import APP_NAME, VERSION, POSTGRESQL_CONFIG
from dotenv import load_dotenv


class VerificationWindow(QWidget):
    def __init__(self, db_type):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} - v{VERSION}")
        self.resize(600, 400)
        center_on_screen(self)
        self.db_type = db_type
        self.setFocus()

        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.message_label = QLabel("")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setStyleSheet("font-size: 14px; color: orange;")
        content_layout.addWidget(self.message_label)

        self.setLayout(content_layout)

        QTimer.singleShot(100, self.verifier_et_ouvrir)

    def verifier_et_ouvrir(self):
        load_dotenv(override=True)

        if self.db_type == "PostgreSQL":
            db_config = POSTGRESQL_CONFIG()
            connection, error = connect_to_sql_database(db_config)
            if connection:
                self.message_label.setText("Connexion réussie !")
                QApplication.processEvents()
                fade_widget(self, duration=500, fade_in=False, finished_callback=self.afficher_login_window)
            else:
                self.message_label.setText(f"Connexion échouée :\nVeuillez configurer la base.")
                QApplication.processEvents()
                fade_widget(self, duration=500, fade_in=False, finished_callback=self.afficher_configuration_window)
        else:
            self.message_label.setText(f"Type de base de donnée non supporté : {self.db_type}")
            QApplication.processEvents()

    def afficher_login_window(self):
        self.hide()
        from main.page.page_1_bdd.select_bdd import ChoixBDDWindow
        self.main_window = ChoixBDDWindow()
        self.main_window.show()
        fade_widget(self.main_window, duration=500, fade_in=True)
        QTimer.singleShot(1000, self.deleteLater)

    def afficher_configuration_window(self):
        self.hide()
        self.config_window = ConfigurationWindow(db_type=self.db_type)
        self.config_window.show()
        fade_widget(self.config_window, duration=500, fade_in=True)
        QTimer.singleShot(1000, self.deleteLater)
