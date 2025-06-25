import sys
from pathlib import Path
from settings import APP_NAME, VERSION
from main.utils.module.maria_db import connect_to_maria_database, MARIA_DB_CONFIG
from main.utils.module.postgres import connect_to_postgresql_database, POSTGRESQL_CONFIG
from main.utils.module.mongo_db import connect_to_mongo, MONGO_DB_CONFIG, voir_collections_mongo
from main.utils.fonction_diverse import Close
from main.utils.regles_visuelles.fad_widjet import fade_widget

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt, QTimer

# Gestion du chemin
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(Path(__file__).resolve().parent / "main"))


class Menu_bddWindow(QWidget):
    def __init__(self, style_base_donné, connection_mongo, choix_bdd):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} - {VERSION}")
        self.resize(600, 400)
        self.style_base_donné = style_base_donné
        self.choix_bdd = choix_bdd
        self.connection_mongo = connection_mongo

        self.setFocus()
        content_layout = QVBoxLayout()

        self.Menu_label = QLabel("Gestion de la base de données")
        self.Menu_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.Menu_label.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        content_layout.addWidget(self.Menu_label)

        self.message_label = QLabel("Sélectionner une action :")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setStyleSheet("font-size: 14px; color: orange;")
        content_layout.addWidget(self.message_label)

        self.button_contenu_bdd = self.creer_bouton("Contenu de la bdd", self.afficher_contenu_bdd)
        self.button_chercher_dans_bdd = self.creer_bouton("Recherche dans la bdd", self.chercher_dans_bdd)
        self.button_faire_une_requete_sql = self.creer_bouton(
            "Faire une requête SQL", self.faire_une_requete_sql,
            extra_style="font-size: 14px; padding: 5px;"
        )
        self.retour_button = self.creer_bouton("Retour", self.retour, min_width=200, max_width=300)

        horizontal_layout = QHBoxLayout()
        horizontal_layout.addWidget(self.button_contenu_bdd)
        horizontal_layout.addWidget(self.button_chercher_dans_bdd)
        horizontal_layout.addWidget(self.button_faire_une_requete_sql)
        content_layout.addLayout(horizontal_layout)

        content_layout.addWidget(self.retour_button, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(content_layout)

    def creer_bouton(self, texte, slot, min_width=200, max_width=300, min_height=30, max_height=45, extra_style=""):
        bouton = QPushButton(texte)
        bouton.setMinimumSize(min_width, min_height)
        bouton.setMaximumSize(max_width, max_height)
        bouton.setStyleSheet(extra_style)
        bouton.clicked.connect(slot)
        return bouton

    def afficher_contenu_bdd(self):
        error = None
        connection = None
        cursor = None

        try:
            if self.style_base_donné == "PostgreSQL":
                db_config = POSTGRESQL_CONFIG(dbname=self.choix_bdd)
                connection, error = connect_to_postgresql_database(db_config)
                if connection:
                    cursor = connection.cursor()
                    cursor.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public';")
                    table_names = [row[0] for row in cursor.fetchall()]
                    self.ouvrir_gestion_table(table_names)
                else:
                    self.message_label.setText(f"Erreur de connexion PostgreSQL : {error}")

            elif self.style_base_donné == "MariaDB":
                db_config = MARIA_DB_CONFIG(dbname=self.choix_bdd)
                connection, error = connect_to_maria_database(db_config)
                if connection:
                    cursor = connection.cursor()
                    cursor.execute(f"SHOW TABLES FROM `{self.choix_bdd}`;")
                    table_names = [row[0] for row in cursor.fetchall()]
                    self.ouvrir_gestion_table(table_names)
                else:
                    self.message_label.setText(f"Erreur de connexion MariaDB : {error}")

            elif self.style_base_donné == "MongoDB":
                if self.connection_mongo:
                    try:
                        table_names = voir_collections_mongo(self.connection_mongo, self.choix_bdd)
                        self.ouvrir_gestion_table(table_names)
                    except Exception as e:
                        self.message_label.setText(f"Erreur MongoDB : {e}")
                        print(f"Erreur MongoDB : {e}")
                else:
                    self.message_label.setText("Connexion MongoDB non disponible.")
            else:
                self.message_label.setText(f"Type de base non supporté : {self.style_base_donné}")

        except Exception as e:
            self.message_label.setText(f"Erreur lors de la récupération des tables : {e}")
            print(f"Erreur globale : {e}")

        finally:
            if connection and cursor and self.style_base_donné != "MongoDB":
                Close(connection, cursor)

    def chercher_dans_bdd(self):
        self.message_label.setText("Recherche en développement...")

    def faire_une_requete_sql(self):
        self.hide()
        from main.page.differente_bdd.page_sql import SQL_Window
        self.sql_window = SQL_Window(self.style_base_donné, self.choix_bdd)
        self.sql_window.show()
        fade_widget(self.sql_window, duration=500, fade_in=True)
        QTimer.singleShot(1000, self.deleteLater)

    def retour(self):
        self.hide()
        from main.page.menu_principal_bdd import Menu_Principal_Window
        self.main_window = Menu_Principal_Window(self.style_base_donné, self.choix_bdd)
        self.main_window.show()
        fade_widget(self.main_window, duration=500, fade_in=True)
        QTimer.singleShot(1000, self.deleteLater)

    def ouvrir_gestion_table(self, table_name):
        self.hide()
        from main.page.gestion_table import GestionTableWindow
        self.gestion_table_window = GestionTableWindow(
            self.style_base_donné,
            self.connection_mongo if self.style_base_donné == "MongoDB" else None,
            self.choix_bdd,
            table_name=table_name,
        )
        self.gestion_table_window.show()
        fade_widget(self.gestion_table_window, duration=500, fade_in=True)
        QTimer.singleShot(1000, self.deleteLater)
