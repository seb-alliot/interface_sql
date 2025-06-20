import sys
from pathlib import Path
from dotenv import load_dotenv
project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))
# --- Fin de la correction ---

from main.utils.gestion_bdd.connection_db import connect_to_postgresql_database

from settings import POSTGRESQL_CONFIG
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,  QTableWidget, QTableWidgetItem, QTextEdit, QHeaderView
)
from PyQt6.QtCore import Qt, QTimer
from main.utils import Close

class SQL_Window(QWidget):
    def __init__(self,db_type, dbname):
        super().__init__()
        self.setWindowTitle("Console SQL")
        self.resize(800, 600)

        self.dbname = dbname
        self.db_type = db_type
        self.config = POSTGRESQL_CONFIG(dbname=dbname)

        layout = QVBoxLayout()

        self.zone_sql = QTextEdit()
        self.zone_sql.setPlaceholderText("Entrez votre requête SQL ici...")
        layout.addWidget(self.zone_sql)

        self.bouton_exec = QPushButton("Exécuter la requête")
        self.bouton_exec.clicked.connect(self.executer_requete)
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
        from main.utils import Close
        Close(self)
        from main.page.menu_bdd import Menu_bddWindow
        self.menu_window = Menu_bddWindow(self.dbname, self.db_type)
        self.menu_window.show()
        self.close()

    def executer_requete(self):
        requete = self.zone_sql.toPlainText().strip()
        if not requete:
            self.label_info.setText("Aucune requête à exécuter.")
            return

        connexion, erreur = connect_to_postgresql_database(self.config)
        if not connexion:
            self.label_info.setText(f"Erreur de connexion : {erreur}")
            return

        curseur = connexion.cursor()
        try:
            curseur.execute(requete)

            if curseur.description:  # SELECT
                resultats = curseur.fetchall()
                noms_colonnes = [desc[0] for desc in curseur.description]
                self.afficher_resultat(resultats, noms_colonnes)
                self.label_info.setText("Requête exécutée avec succès.")
            else:  # INSERT, UPDATE, DELETE
                connexion.commit()
                self.resultat_table.setRowCount(0)
                self.resultat_table.setColumnCount(0)
                self.label_info.setText("Requête exécutée avec succès (aucun résultat).")

        except Exception as e:
            self.label_info.setText(f"Erreur : {e}")
        finally:
            Close(connexion, curseur)

    def afficher_resultat(self, lignes, colonnes):
        self.resultat_table.clear()
        self.resultat_table.setRowCount(len(lignes))
        self.resultat_table.setColumnCount(len(colonnes))
        self.resultat_table.setHorizontalHeaderLabels(colonnes)

        for i, ligne in enumerate(lignes):
            for j, valeur in enumerate(ligne):
                item = QTableWidgetItem(str(valeur))
                self.resultat_table.setItem(i, j, item)

        self.resultat_table.resizeColumnsToContents()
        self.resultat_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
