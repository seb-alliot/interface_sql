import sys
from pathlib import Path
from dotenv import load_dotenv

project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from main.utils.gestion_bdd.affichage_table import recuperer_tables
from main import center_on_screen
from main.utils.regles_visuelles.fad_widjet import fade_widget

from settings import APP_NAME, VERSION
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt, QTimer
from main.utils.fonction_diverse import Close
from main.utils.fonction_diverse import importer_module_bdd


class Afficher_Table_SQL_Window(QWidget):
    def __init__(self, style_base_donne, connection, choix_bdd, table_name):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} - {VERSION}")
        self.resize(600, 400)
        center_on_screen(self)

        self.style_base_donne = style_base_donne
        self.choix_bdd = choix_bdd
        self.table_name = table_name
        self.connection = connection

        # Import dynamique du module adapté à la BDD
        self.module = importer_module_bdd(self.style_base_donne)
        self.module_query = self.module.import_query_module("voir_contenu_table")


        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title_label = QLabel(f"Affichage de la table {self.table_name} dans la base de données {self.choix_bdd}.")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
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
        if not self.connection:
            self.message_label.setText("Aucune connexion active.")
            return

        if self.style_base_donne == "MongoDB":
            connection = self.connection
        else:
            connection = self.connection[0]

        if not connection:
            self.message_label.setText("Connexion invalide.")
            return

        if self.style_base_donne == "MongoDB":
            try:
                table = self.table_name[0] if isinstance(self.table_name, list) else self.table_name
                contenu = self.module_query.voir_contenu_table(connection, self.choix_bdd, table)

                if isinstance(contenu, dict):
                    contenu = [contenu]
                elif not isinstance(contenu, list):
                    raise ValueError("Le contenu doit être une liste ou un dictionnaire.")

                if not contenu:
                    self.message_label.setText(f"La collection {table} est vide ou inexistante.")
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
                self.message_label.setText(f"{len(contenu)} documents affichés depuis {table}")

            except Exception as e:
                self.message_label.setText(f"Erreur MongoDB : {e}")
            return

        # Partie SQL
        table_names = [self.table_name] if isinstance(self.table_name, str) else self.table_name
        for table in table_names:
            if not table:
                self.message_label.setText("Aucune table présente.")
                return
            try:
                cursor = connection.cursor()
                cursor.execute(self.module_query.voir_contenu_table(table))
                toutes_les_lignes = cursor.fetchall()
                noms_colonnes = [info[0] for info in cursor.description]

                self.table_tableau.setRowCount(len(toutes_les_lignes))
                self.table_tableau.setColumnCount(len(noms_colonnes))
                self.table_tableau.setHorizontalHeaderLabels(noms_colonnes)

                for colonnes, ligne in enumerate(toutes_les_lignes):
                    for clef, valeur in enumerate(ligne):
                        self.table_tableau.setItem(colonnes, clef, QTableWidgetItem(str(valeur)))

                self.table_tableau.resizeColumnsToContents()
                self.table_tableau.resizeRowsToContents()
                self.message_label.setText(f"Contenu de la table {table} affiché avec succès.")
            except Exception as e:
                self.message_label.setText(f"Erreur SQL : {e}")

    def retour(self):
        self.message_label.setText("Retour à la sélection de la table...")
        self.hide()

        from main.page.gestion_table import GestionTableWindow
        self.main_window = GestionTableWindow(
            self.style_base_donne,
            self.connection,
            self.choix_bdd,
            table_name=recuperer_tables(
                self.style_base_donne,
                self.connection,
                self.choix_bdd)
        )

        self.main_window.show()
        fade_widget(self.main_window, duration=500, fade_in=True)
        QTimer.singleShot(1000, self.deleteLater)

    def closeEvent(self, event):
        Close(self, event)
