import sys
from pathlib import Path
from dotenv import load_dotenv

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from main.utils.module.maria_db import connect_to_maria_database, MARIA_DB_CONFIG, voir_base_maria, voir_contenu_maria
from main.utils.module.postgres import connect_to_postgresql_database, POSTGRESQL_CONFIG, voir_base_postgresql, voir_contenu_table_postgres
from main.utils.module.mongo_db import connect_to_mongo, MONGO_DB_CONFIG
from main.utils.module.mongo_db import voir_contenu_collection_mongo
from main.utils.gestion_bdd.affichage_table import recuperer_tables
from main import center_on_screen
from main.utils.regles_visuelles.fad_widjet import fade_widget

from settings import APP_NAME, VERSION
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt, QTimer
from main.utils.fonction_diverse import Close

# Configurations pour PostgreSQL et MariaDB uniquement
db_configs = {
    "PostgreSQL": {
        "config_bdd": POSTGRESQL_CONFIG,
        "connector": connect_to_postgresql_database,
        "query_bdd": voir_base_postgresql,
        "query_table": voir_contenu_table_postgres,
    },
    "MariaDB": {
        "config_bdd": MARIA_DB_CONFIG,
        "connector": connect_to_maria_database,
        "query_bdd": voir_base_maria,
        "query_table": voir_contenu_maria,
    },
    "MongoDB": {
        "config_bdd": MONGO_DB_CONFIG,
        "connector": None,
        "query_bdd": None,
        "query_table": voir_contenu_collection_mongo,
    }
}

class Afficher_Table_SQL_Window(QWidget):
    def __init__(self, style_base_donné, connection, choix_bdd, table_name):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} - {VERSION}")
        self.resize(600, 400)
        center_on_screen(self)

        self.style_base_donné = style_base_donné
        self.choix_bdd = choix_bdd
        self.table_name = table_name[0] if isinstance(table_name, list) else table_name
        self.connection = connection

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title_label = QLabel(f"Affichage de la table {self.table_name} dans la base de données {self.choix_bdd}.")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: black;")
        layout.addWidget(self.title_label)

        self.message_label = QLabel("")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setStyleSheet("font-size: 14px; color: orange;")
        layout.addWidget(self.message_label)

        self.table_tableau = QTableWidget()
        layout.addWidget(self.table_tableau)

        self.button_return = QPushButton("Retour au menu")
        self.button_return.setStyleSheet("font-size: 14px; color: white;")
        self.button_return.clicked.connect(self.retour)
        layout.addWidget(self.button_return)

        self.setLayout(layout)
        self.afficher_contenu_table()

    def afficher_contenu_table(self):
        choix = self.style_base_donné

        if choix == "MongoDB":
            try:
                if self.connection is None:
                    self.message_label.setText(f"Connexion échouée : MongoDB non connecté.")
                    return

                contenu = voir_contenu_collection_mongo(self.connection, self.choix_bdd, self.table_name)

                if not contenu:
                    self.message_label.setText(f"La collection {self.table_name} est vide ou inexistante.")
                    return

                colonnes = list({clef for document in contenu for clef in document.keys()})
                self.table_tableau.setColumnCount(len(colonnes))
                self.table_tableau.setRowCount(len(contenu))
                self.table_tableau.setHorizontalHeaderLabels(colonnes)

                for ligne, document in enumerate(contenu):
                    for col, cle in enumerate(colonnes):
                        valeur = document.get(cle, "")
                        self.table_tableau.setItem(ligne, col, QTableWidgetItem(str(valeur)))

                self.table_tableau.resizeColumnsToContents()
                self.message_label.setText(f"{len(contenu)} documents affichés depuis {self.table_name}")
            except Exception as e:
                self.message_label.setText(f"Erreur MongoDB : {e}")
            return

        if choix in db_configs:
            try:
                connection, erreur = self.connection, None
                query_table = db_configs[choix]["query_table"]

                if not connection:
                    self.message_label.setText(f"Connexion échouée : {erreur}")
                    return

                curseur = connection.cursor()
                curseur.execute(query_table(self.table_name))
                toutes_les_lignes = curseur.fetchall()
                noms_colonnes = [info[0] for info in curseur.description]

                self.table_tableau.setRowCount(len(toutes_les_lignes))
                self.table_tableau.setColumnCount(len(noms_colonnes))
                self.table_tableau.setHorizontalHeaderLabels(noms_colonnes)

                for i, ligne in enumerate(toutes_les_lignes):
                    for j, valeur in enumerate(ligne):
                        self.table_tableau.setItem(i, j, QTableWidgetItem(str(valeur)))

                self.table_tableau.resizeColumnsToContents()
                self.table_tableau.resizeRowsToContents()
                self.message_label.setText(f"Contenu de la table {self.table_name} affiché avec succès.")
            except Exception as e:
                print(f"Erreur SQL ({self.table_name}) : {e}")
                self.message_label.setText(f"Erreur SQL : {e}")
        else:
            self.message_label.setText("Type de base de données non pris en charge.")

    def retour(self):
        self.message_label.setText("Retour à la sélection de la table...")
        self.hide()

        from main.page.gestion_table import GestionTableWindow
        self.main_window = GestionTableWindow(
            self.style_base_donné,
            self.connection,
            self.choix_bdd,
            table_name=recuperer_tables(
                self.style_base_donné,
                self.connection,
                self.choix_bdd)
        )

        self.main_window.show()
        fade_widget(self.main_window, duration=500, fade_in=True)
        QTimer.singleShot(1000, self.deleteLater)
