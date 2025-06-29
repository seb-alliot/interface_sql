import sys
from pathlib import Path
from dotenv import load_dotenv
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QTableWidget, QTableWidgetItem, QTextEdit, QHeaderView
)
from PyQt6.QtCore import Qt

from main.utils.fonction_diverse.import_modul import importer_module_bdd
from main.utils import Close
from main.utils.gestion_bdd.affichage_table import recuperer_tables

# Chargement des variables d’environnement
project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

load_dotenv(dotenv_path=project_root / ".env")


class Requete_sql_sur_table(QWidget):
    def __init__(self, style_base_donné, connection, choix_bdd , table_name):
        super().__init__()
        self.setWindowTitle("Console SQL")
        self.resize(800, 600)

        self.style_base_donné = style_base_donné
        self.module = importer_module_bdd(self.style_base_donné)
        self.connection = connection
        self.choix_bdd = choix_bdd
        self.table_name = table_name

        layout = QVBoxLayout()

        self.zone_sql = QTextEdit()
        self.zone_sql.setPlaceholderText("Entrez votre requête SQL ici...")
        layout.addWidget(self.zone_sql)

        self.bouton_exec = QPushButton("Exécuter la requête")
        layout.addWidget(self.bouton_exec)

        self.label_info = QLabel("")
        self.label_info.setStyleSheet("color: orange; font-weight: bold")
        layout.addWidget(self.label_info)

        self.resultat_table = QTableWidget()
        layout.addWidget(self.resultat_table)

        self.button_retour = QPushButton("Retour au menu")
        self.button_retour.setStyleSheet("font-size: 14px; color: white;")
        self.button_retour.clicked.connect(self.retour_menu)
        layout.addWidget(self.button_retour)

        self.setLayout(layout)

    def retour_menu(self):
        self.hide()
        from main.page.gestion_table import GestionTableWindow
        self.menu_window = GestionTableWindow(
            self.style_base_donné,
            self.connection,
            self.choix_bdd,
            table_name= recuperer_tables(
                self.style_base_donné,
                self.connection,
                self.choix_bdd
            )
        )
        self.menu_window.show()
        self.close()

    def closeEvent(self, event):
        Close(self, event)