import sys
from pathlib import Path
from dotenv import load_dotenv
project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))
# --- Fin de la correction ---

from main.utils.gestion_bdd.connection_db import connect_to_postgresql_database
from main import center_on_screen
from main.utils.regles_visuelles.fad_widjet import fade_widget

from settings import APP_NAME, VERSION, POSTGRES_DB, MAJ_DB_CONFIG, POSTGRESQL_CONFIG
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QTableWidget, QTableWidgetItem
)
from PyQt6.QtCore import Qt, QTimer
from main.utils.fonction_diverse import Close



class Afficher_Table_SQL_Window(QWidget):
    def __init__(self, db_type, table_name):
        print(f" donnée transmise : {db_type} - {table_name}")
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} - {VERSION}")
        self.resize(600, 400)
        center_on_screen(self)
        self.db_type = db_type
        self.dbname = db_type
        self.table_name = table_name[0] if isinstance(table_name, list) else table_name

        self.setFocus()

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title_label = QLabel(f"Affichage de la table {self.table_name} dans la base de données {self.dbname}.")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: black;")
        layout.addWidget(self.title_label)


        # Message d’info ou d’erreur
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
        config = POSTGRESQL_CONFIG(dbname=self.dbname)
        print("Base de données utilisée :", config["dbname"])
        if not config:
            self.message_label.setText("Aucune base de données sélectionnée.")
            return
        try:
            connexion, erreur = connect_to_postgresql_database(config)
            if not connexion:
                self.message_label.setText(f"Échec de la connexion à la base de données : {erreur}")
                return

            curseur = connexion.cursor()
            curseur.execute(f"SELECT * FROM {self.table_name};")
            toutes_les_lignes = curseur.fetchall()
            noms_colonnes = [info_colonne[0] for info_colonne in curseur.description]

            self.table_tableau.setRowCount(len(toutes_les_lignes))
            self.table_tableau.setColumnCount(len(noms_colonnes))
            self.table_tableau.setHorizontalHeaderLabels(noms_colonnes)

            for indice_ligne, ligne in enumerate(toutes_les_lignes):
                for indice_colonne, valeur_cellule in enumerate(ligne):
                    item = QTableWidgetItem(str(valeur_cellule))
                    self.table_tableau.setItem(indice_ligne, indice_colonne, item)

            self.table_tableau.resizeColumnsToContents()
            self.table_tableau.resizeRowsToContents()

            Close(connexion, curseur)
            self.message_label.setText(f"Contenu de la table {self.table_name} affiché avec succès.")
        except Exception as e:
            print(f"Erreur lors de l'affichage de la table {self.table_name} : {str(e)}")
            self.message_label.setText(f"Erreur lors de l'affichage de la table : {str(e)}")

    def afficher_contenu_bdd(self):
        db_config = POSTGRESQL_CONFIG(dbname=self.dbname)
        connection, error = connect_to_postgresql_database(db_config)
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public';")
                table_names = [table[0] for table in cursor.fetchall()]
                return table_names
            except Exception as e:
                self.message_label.setText(f"Erreur lors de la récupération des tables : {e}")
            finally:
                Close(connection, cursor)
        else:
            self.message_label.setText(f"Erreur de connexion à la base de données : {error}")

    def retour(self):
        table_name= self.afficher_contenu_bdd()
        if not table_name:
            self.message_label.setText("Aucune table trouvée dans la base de données.")
            return
        self.message_label.setText("Retour a la selection de la table...")
        self.hide()
        from main.page.gestion_table import GestionTableWindow

        self.main_window = GestionTableWindow(dbname=self.dbname,db_type=self.db_type, table_name=table_name)
        self.main_window.show()
        fade_widget(self.main_window, duration=500, fade_in=True)
        QTimer.singleShot(1000, self.deleteLater)



if __name__ == "__main__":
    app = QApplication(sys.argv)

    fenetre = Afficher_Table_SQL_Window()
    fenetre.show()

    sys.exit(app.exec())
