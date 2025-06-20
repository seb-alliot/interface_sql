import sys
from pathlib import Path
from settings import APP_NAME, VERSION , POSTGRESQL_CONFIG, MARIA_DB_CONFIG
from main.utils.gestion_bdd.connection_db import connect_to_postgresql_database, connect_to_maria_database
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(Path(__file__).resolve().parent / "main"))

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt, QTimer
from main.utils import Close
from main.utils.regles_visuelles.fad_widjet import fade_widget


class Menu_bddWindow(QWidget):
    def __init__(self,db_type, select_bdd=None):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} - {VERSION}")
        self.resize(600, 400)
        self.select_bdd = select_bdd
        self.db_type = db_type
        content_layout = QVBoxLayout()

        self.Menu_label = QLabel("Gestion de la base de données")
        self.Menu_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.Menu_label.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        content_layout.addWidget(self.Menu_label)

        self.message_label = QLabel("Selectionner une action :")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setStyleSheet("font-size: 14px; color: orange;")
        content_layout.addWidget(self.message_label)

        self.button_contenu_bdd = self.creer_bouton("Contenu de la bdd", self.afficher_contenu_bdd)
        self.button_chercher_dans_bdd = self.creer_bouton("Recherche dans la bdd", self.chercher_dans_bdd)
        self.button_faire_une_requete_sql = self.creer_bouton("Faire une requête SQL", self.faire_une_requete_sql,
        extra_style="font-size: 14px; padding: 5px;")
        self.retour_button = self.creer_bouton("Retour", self.retour, min_width=200, max_width=300)

        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(self.button_contenu_bdd)
        horizontal_layout.addWidget(self.button_chercher_dans_bdd)
        horizontal_layout.addWidget(self.button_faire_une_requete_sql)
        content_layout.addLayout(horizontal_layout)

        content_layout.addWidget(self.button_faire_une_requete_sql, alignment=Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(self.retour_button, alignment=Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(self.message_label)

        self.setLayout(content_layout)

    def creer_bouton(self, texte, slot, min_width=200, max_width=300, min_height=45, max_height=30, extra_style=""):
        bouton = QPushButton(texte)
        bouton.setMinimumSize(min_width, min_height)
        bouton.setMaximumSize(max_width, max_height)
        bouton.setStyleSheet(extra_style)
        bouton.clicked.connect(slot)
        return bouton


    def afficher_contenu_bdd(self):
        if self.db_type == "PostgreSQL":
            db_config = POSTGRESQL_CONFIG(dbname=self.select_bdd)
            connection, error = connect_to_postgresql_database(db_config)
        elif self.db_type == "MariaDB":
            db_config = MARIA_DB_CONFIG(dbname=self.select_bdd)
            print(f"Configuration de la base de données : {db_config} et la base de données sélectionnée : {self.select_bdd}")
            connection, error = connect_to_maria_database(db_config)
        else:
            self.message_label.setText(f"Type de base non supporté : {self.db_type}")
            return

        if connection:
            try:
                cursor = connection.cursor()
                if self.db_type == "PostgreSQL":
                    cursor.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public';")
                elif self.db_type == "MariaDB":
                    cursor.execute(f"SHOW TABLES FROM `{self.select_bdd}`;")
                table_names = [row[0] for row in cursor.fetchall()]
                self.ouvrir_gestion_table(table_names)

            except Exception as e:
                self.message_label.setText(f"Erreur lors de la récupération des tables : {e}")
            finally:
                Close(connection, cursor)
        else:
            self.message_label.setText(f"Erreur de connexion à la base de données : {error}")

    def chercher_dans_bdd(self):
        self.message_label.setText("Recherche en développement...")

    def faire_une_requete_sql(self):
        self.hide()
        from main.page.differente_bdd.page_sql import SQL_Window
        self.sql_window = SQL_Window(db_type=self.db_type, dbname=self.select_bdd)
        self.sql_window.show()
        fade_widget(self.sql_window, duration=500, fade_in=True)
        QTimer.singleShot(1000, self.deleteLater)

    def retour(self):
        self.hide()
        from main.page.menu import MenuWindow
        self.main_window = MenuWindow(db_type=self.db_type, select_bdd=self.select_bdd)
        self.main_window.show()
        fade_widget(self.main_window, duration=500, fade_in=True)
        QTimer.singleShot(1000, self.deleteLater)

    def ouvrir_gestion_table(self, table_name):
        self.hide()
        from main.page.gestion_table import GestionTableWindow
        self.gestion_table_window = GestionTableWindow(db_type=self.db_type, table_name=table_name, dbname=self.select_bdd)
        self.gestion_table_window.show()
        fade_widget(self.gestion_table_window, duration=500, fade_in=True)
        QTimer.singleShot(1000, self.deleteLater)


if __name__ == "__main__":
    app = QApplication([])
    fenetre = Menu_bddWindow()
    fenetre.show()
    app.exec()
