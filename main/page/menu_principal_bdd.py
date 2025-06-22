import sys
from pathlib import Path
from settings import APP_NAME, VERSION
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(Path(__file__).resolve().parent / "main"))
from main.utils.fonction_diverse.recharge_env import recharger_env
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton
)
from PyQt6.QtCore import Qt , QTimer
from main.utils.module.maria_db import connect_to_maria_database, MARIA_DB_CONFIG, MARIA_AUTO_CONNECT, voir_base_maria
from main.utils.module.postgres import connect_to_postgresql_database, POSTGRESQL_CONFIG, POSTGRESQL_AUTO_CONNECT, voir_base_postgresql
from main.utils import Close



# Dictionnaire factorisé de la configuration des bases de données
db_configs = {
    "PostgreSQL": {
    "config_bdd": POSTGRESQL_CONFIG,
    "connector": connect_to_postgresql_database,
    "query": voir_base_postgresql,
    },
    "MariaDB": {
    "config_bdd": MARIA_DB_CONFIG,
    "connector": connect_to_maria_database,
    "query": voir_base_maria
    }
}

class Menu_Principal_Window(QWidget):
    def __init__(self , style_base_donné, choix_bdd=None):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} - {VERSION}")
        self.resize(600, 400)
        self.setFocus()
        self.style_base_donné = style_base_donné
        print("_" * 40)
        print("Menu Principal BDD")
        print(f"style_base_donné : {self.style_base_donné}")
        self.choix_bdd = choix_bdd if choix_bdd else "Base de données non sélectionnée"
        print(f"choix_bdd : {self.choix_bdd}")

        layout = QVBoxLayout()

        self.Menu_label = QLabel("Menu principal")
        self.Menu_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.Menu_label)

        self.label_bdd = QLabel("Choisissez une base de donnée :")
        layout.addWidget(self.label_bdd)

        self.choix_bdd = QComboBox()
        self.choix_bdd.addItems(self.list_bdd())
        self.choix_bdd.setMinimumWidth(200)
        self.choix_bdd.setMaximumWidth(300)
        self.choix_bdd.setMinimumHeight(30)
        self.choix_bdd.setMaximumHeight(45)
        self.choix_bdd.setStyleSheet("font-size: 14px; padding: 5px;")
        layout.addWidget(self.choix_bdd)

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
        from main.page.selection_style_bdd import ChoixBDDWindow
        self.main_window = ChoixBDDWindow()
        self.main_window.show()
        from main.utils.regles_visuelles.fad_widjet import fade_widget
        fade_widget(self.main_window, duration=500, fade_in=True)
        QTimer.singleShot(1000, self.deleteLater)

    def list_bdd(self):
        if self.style_base_donné not in db_configs:
            return ["Base de données non supportée"]

        # Récupération des infos via la clé
        dictionnaire_config = db_configs[self.style_base_donné]
        connection_bdd, erreur = dictionnaire_config["connector"](dictionnaire_config["config_bdd"]())
        query = dictionnaire_config["query"]

        if isinstance(connection_bdd, str):
            return [connection_bdd]

        try:
            cursor = connection_bdd.cursor()
            cursor.execute(query())
            return [bdd[0] for bdd in cursor.fetchall()]
        except Exception:
            return ["Erreur lors de la récupération des bases de données"]
        finally:
            Close(cursor, connection_bdd)


    def retour_menu_bdd(self):
        self.hide()
        from main.page.choix_bdd import Menu_bddWindow
        self.main_window = Menu_bddWindow(choix_bdd=self.choix_bdd.currentText(), style_base_donné=self.style_base_donné)
        self.main_window.show()
        from main.utils.regles_visuelles.fad_widjet import fade_widget
        fade_widget(self.main_window, duration=500, fade_in=True)
        QTimer.singleShot(1000, self.deleteLater)

    def connection_bdd(self):
        recharger_env()

        choix_bdd = self.choix_bdd.currentText()
        if not choix_bdd or choix_bdd == "Base de données non sélectionnée":
            self.label_bdd.setText("Veuillez sélectionner une base de données valide.")
            return

        if self.style_base_donné not in db_configs:
            self.label_bdd.setText("Type de base de données non reconnu.")
            return

        config = db_configs[self.style_base_donné]
        db_config = config["config_bdd"]()

        try:
            connection, error = config["connector"](db_config)

            if error:
                self.label_bdd.setText(f"Erreur de connexion : {error}")
                return

            if not connection:
                self.label_bdd.setText("La connexion a échoué.")
                return

            # Si tout est ok, fermer la connexion et passer à la suite
            connection.close()
            self.label_bdd.setText(f"Connexion réussie à '{choix_bdd}'")
            self.retour_menu_bdd()

        except Exception as e:
            self.label_bdd.setText(f"Erreur lors de la connexion : {str(e)}")

    def configuration_bdd(self):
            self.hide()
            from main.page.configuration import ConfigurationWindow
            self.main_window = ConfigurationWindow(self.style_base_donné)
            self.main_window.show()
            from main.utils.regles_visuelles.fad_widjet import fade_widget
            fade_widget(self.main_window, duration=500, fade_in=True)
            QTimer.singleShot(1000, self.deleteLater)
