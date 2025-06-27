import sys
from pathlib import Path
from settings import APP_NAME, VERSION

project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(Path(__file__).resolve().parent / "main"))

from main.utils.fonction_diverse.recharge_env import recharger_env
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton
from PyQt6.QtCore import Qt, QTimer
from main.utils.module.maria_db import connect_to_maria_database, MARIA_DB_CONFIG, voir_base_maria
from main.utils.module.postgres import connect_to_postgresql_database, POSTGRESQL_CONFIG, voir_base_postgresql
from main.utils.module.mongo_db import voir_collections_mongo
from main.utils import Close

# Dictionnaire factorisé de la configuration des bases de données
db_configs = {
    "PostgreSQL": {
        "config_bdd": POSTGRESQL_CONFIG,
        "connecteur": connect_to_postgresql_database,
        "query": voir_base_postgresql,
    },
    "MariaDB": {
        "config_bdd": MARIA_DB_CONFIG,
        "connecteur": connect_to_maria_database,
        "query": voir_base_maria
    },
    "MongoDB": {
        "config_bdd": None,
        "connecteur": None,
        "query": voir_collections_mongo,
    }
}

class Menu_Principal_Window(QWidget):
    def __init__(self, style_base_donné, connection, choix_bdd=None):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} - {VERSION}")
        self.resize(600, 400)
        self.setFocus()
        self.style_base_donné = style_base_donné
        self.connection = connection
        print(f"Connection menu principal : {self.connection}")
        self.choix_bdd = choix_bdd

        layout = QVBoxLayout()

        self.Menu_label = QLabel("Menu principal")
        self.Menu_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.Menu_label)

        self.label_bdd = QLabel("Choisissez une base de donnée :")
        layout.addWidget(self.label_bdd)

        self.choix_bdd_combo = QComboBox()
        self.choix_bdd_combo.addItems(self.list_bdd())
        self.choix_bdd_combo.setMinimumWidth(200)
        self.choix_bdd_combo.setMaximumWidth(300)
        self.choix_bdd_combo.setMinimumHeight(30)
        self.choix_bdd_combo.setMaximumHeight(45)
        self.choix_bdd_combo.setStyleSheet("font-size: 14px; padding: 5px;")
        layout.addWidget(self.choix_bdd_combo)

        # Bouton connexion
        content_layout = QVBoxLayout()
        self.bouton_connection_bdd = QPushButton("Connexion à la BDD")
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bouton_connection_bdd.setMinimumSize(200, 30)
        self.bouton_connection_bdd.clicked.connect(self.connection_bdd)
        content_layout.addWidget(self.bouton_connection_bdd)
        layout.addLayout(content_layout)

        # Bouton configuration
        content_layout = QVBoxLayout()
        self.validation_button = QPushButton("Configuration")
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.validation_button.setMinimumSize(200, 30)
        self.validation_button.clicked.connect(self.configuration_bdd)
        content_layout.addWidget(self.validation_button)
        layout.addLayout(content_layout)

        # Bouton retour
        content_layout = QVBoxLayout()
        self.retour_button = QPushButton("Retour")
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.retour_button.setMinimumSize(200, 30)
        self.retour_button.clicked.connect(self.retour)
        content_layout.addWidget(self.retour_button)
        layout.addLayout(content_layout)

        self.setLayout(layout)

    def retour(self):
        self.hide()
        if self.connection:
            self.connection.close()
        from main.page.selection_style_bdd import ChoixBDDWindow
        self.main_window = ChoixBDDWindow(
            connection=self.connection,
        )
        self.main_window.show()
        from main.utils.regles_visuelles.fad_widjet import fade_widget
        fade_widget(self.main_window, duration=500, fade_in=True)
        QTimer.singleShot(1000, self.deleteLater)

    def list_bdd(self):
        if self.style_base_donné not in db_configs:
            return ["Base de données non supportée"]

        config = db_configs[self.style_base_donné]
        connection = self.connection
        try:
            if self.style_base_donné == "MongoDB":
                client = self.connection
                return client.list_database_names()
            elif not connection:
                return ["Aucune connexion active"]
            else:

                cursor = self.connection.cursor()
                cursor.execute(config["query"]())
                return [bdd[0] for bdd in cursor.fetchall()]

        except Exception as e:
            return [f"Erreur : {str(e)}"]

    def connection_bdd(self):
        recharger_env()
        connection = self.connection
        nouvelle_connection = None

        if not connection:
            self.label_bdd.setText("Aucune connexion active")
            return
        choix_bdd = self.choix_bdd_combo.currentText()
        if self.style_base_donné == "PostgreSQL":
            nouvelle_connection = connect_to_postgresql_database(POSTGRESQL_CONFIG(dbname=choix_bdd))[0]
        elif self.style_base_donné == "MariaDB":
            nouvelle_connection = connect_to_maria_database(MARIA_DB_CONFIG(dbname=choix_bdd))[0]
        elif choix_bdd == "MongoDB":
            connection = self.connection
        self.connection = nouvelle_connection if nouvelle_connection else connection

        self.retour_menu_bdd()

    def afficher_collections_mongo(self):
        if self.style_base_donné == "MongoDB":
            nom_bdd = self.choix_bdd_combo.currentText()
            collections = voir_collections_mongo(nom_bdd)
            if not collections:
                self.label_bdd.setText(f"Aucune collection trouvée dans '{nom_bdd}'")
                return

            self.label_bdd.setText(f"Collections dans '{nom_bdd}': {', '.join(collections)}")

    def retour_menu_bdd(self):
        self.hide()
        from main.page.choix_bdd import Menu_bddWindow
        self.main_window = Menu_bddWindow(
            style_base_donné=self.style_base_donné,
            connection=self.connection,
            choix_bdd=self.choix_bdd_combo.currentText(),
        )

        self.main_window.show()
        from main.utils.regles_visuelles.fad_widjet import fade_widget
        fade_widget(self.main_window, duration=500, fade_in=True)
        QTimer.singleShot(1000, self.deleteLater)

    def configuration_bdd(self):
        self.hide()
        from main.page.configuration import ConfigurationWindow
        self.main_window = ConfigurationWindow(
            self.style_base_donné,
            connection=self.connection if self.connection else None,
            )
        self.main_window.show()
        from main.utils.regles_visuelles.fad_widjet import fade_widget
        fade_widget(self.main_window, duration=500, fade_in=True)
        QTimer.singleShot(1000, self.deleteLater)

    def closeEvent(self, event):
        Close(self, event)
