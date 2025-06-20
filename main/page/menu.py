import sys
from pathlib import Path
from settings import APP_NAME, VERSION , MAJ_DB_CONFIG, POSTGRESQL_CONFIG, MARIA_DB_CONFIG
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(Path(__file__).resolve().parent / "main"))
from main.utils.fonction_diverse.recharge_env import recharger_env
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton
)
from PyQt6.QtCore import Qt , QTimer
from main.utils.gestion_bdd.connection_db import connect_to_database, connect_to_postgresql_database, connect_to_maria_database
from main.utils import Close

class MenuWindow(QWidget):
    def __init__(self , db_type, select_bdd=None):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} - {VERSION}")
        self.resize(600, 400)
        self.setFocus()
        self.db_type = db_type
        self.select_bdd = select_bdd if select_bdd else "Base de données non sélectionnée"

        layout = QVBoxLayout()

        self.Menu_label = QLabel("Menu principal")
        self.Menu_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.Menu_label)

        self.label_bdd = QLabel("Choisissez une base de donnée :")
        layout.addWidget(self.label_bdd)

        self.select_bdd = QComboBox()
        self.select_bdd.addItems(self.list_bdd())
        self.select_bdd.setMinimumWidth(200)
        self.select_bdd.setMaximumWidth(300)
        self.select_bdd.setMinimumHeight(30)
        self.select_bdd.setMaximumHeight(45)
        self.select_bdd.setStyleSheet("font-size: 14px; padding: 5px;")
        layout.addWidget(self.select_bdd)

        content_layout = QVBoxLayout()
        self.bouton_connection_bdd = QPushButton("Connection a la bdd")
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bouton_connection_bdd.setMinimumSize(200, 30)
        self.bouton_connection_bdd.setMaximumSize(300, 30)
        self.bouton_connection_bdd.setMinimumHeight(30)
        self.bouton_connection_bdd.setMaximumHeight(45)
        self.bouton_connection_bdd.clicked.connect(self.connection_bdd)
        content_layout.addWidget(self.bouton_connection_bdd, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(content_layout)

        content_layout = QVBoxLayout()
        self.validation_button = QPushButton("Configuration")
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.validation_button.setMinimumSize(200, 30)
        self.validation_button.setMaximumSize(300, 30)
        self.validation_button.setMinimumHeight(30)
        self.validation_button.setMaximumHeight(45)
        self.validation_button.clicked.connect(self.configuration_bdd)
        content_layout.addWidget(self.validation_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(content_layout)

        content_layout = QVBoxLayout()
        self.retour_button = QPushButton("Retour")
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.retour_button.setMinimumSize(200, 30)
        self.retour_button.setMaximumSize(300, 30)
        self.retour_button.setMinimumHeight(30)
        self.retour_button.setMaximumHeight(45)
        self.retour_button.clicked.connect(self.retour)
        content_layout.addWidget(self.retour_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(content_layout)
        self.setLayout(layout)

    def retour(self):
        self.hide()
        from main.page.select_bdd import ChoixBDDWindow
        self.main_window = ChoixBDDWindow()
        self.main_window.show()
        from main.utils.regles_visuelles.fad_widjet import fade_widget
        fade_widget(self.main_window, duration=500, fade_in=True)
        QTimer.singleShot(1000, self.deleteLater)

    def list_bdd(self):
        if self.db_type not in ["PostgreSQL","MariaDB", "SQLite"]:
            return ["Base de données non supportée"]
        connection_bdd = None
        erreur = None

        if self.db_type == "PostgreSQL":
            DB_CONFIG = POSTGRESQL_CONFIG()
            connection_bdd, erreur = connect_to_postgresql_database(DB_CONFIG)
            query = "SELECT datname FROM pg_database WHERE datistemplate = false;"
            print(f"Configuration de la base de données : {DB_CONFIG} et la base de données sélectionnée : {self.select_bdd}")
        elif self.db_type == "MariaDB":
            db_config = MARIA_DB_CONFIG(dbname=self.select_bdd)
            print(f"Configuration de la base de données : {db_config} et la base de données sélectionnée : {self.select_bdd}")
            connection_bdd, error = connect_to_maria_database(db_config)
            query = "SHOW DATABASES;"
        if connection_bdd is None or not connection_bdd:
            return ["Aucune base de données disponible"]

        if isinstance(connection_bdd, str):
            return [connection_bdd]

        try:
            cursor = connection_bdd.cursor()
            cursor.execute(query)
            bdd_list = [bdd[0] for bdd in cursor.fetchall()]
            return bdd_list
        except Exception as e:
            return ["Erreur lors de la récupération des bases de données"]
        finally:
            Close(cursor, connection_bdd)

    def retour_menu_bdd(self):
        self.hide()
        from main.page.menu_bdd import Menu_bddWindow
        self.main_window = Menu_bddWindow(select_bdd=self.select_bdd.currentText(), db_type=self.db_type)
        self.main_window.show()
        from main.utils.regles_visuelles.fad_widjet import fade_widget
        fade_widget(self.main_window, duration=500, fade_in=True)
        QTimer.singleShot(1000, self.deleteLater)

    def connection_bdd(self):
        recharger_env()

        selected_bdd = self.select_bdd.currentText()
        if not selected_bdd or selected_bdd == "Base de données non sélectionnée":
            self.label_bdd.setText("Veuillez sélectionner une base de données valide.")
            return

        if self.db_type == "PostgreSQL":
            DB_CONFIG = POSTGRESQL_CONFIG(dbname=selected_bdd)
            connection_bdd, erreur = connect_to_postgresql_database(DB_CONFIG)
            if connection_bdd:
                self.retour_menu_bdd()
            else:
                self.configuration_bdd()

    def configuration_bdd(self):
            self.hide()
            from main.page.configuration import ConfigurationWindow
            self.main_window = ConfigurationWindow(db_type=self.db_type)
            self.main_window.show()
            from main.utils.regles_visuelles.fad_widjet import fade_widget
            fade_widget(self.main_window, duration=500, fade_in=True)
            QTimer.singleShot(1000, self.deleteLater)

if __name__ == "__main__":
    app = QApplication([])
    fenetre = MenuWindow()
    fenetre.show()
    app.exec()