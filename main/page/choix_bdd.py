import sys
from pathlib import Path
# Gestion du chemin
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from settings import APP_NAME, VERSION
from main.utils.gestion_bdd.affichage_table import recuperer_tables
from main.utils.regles_visuelles.fad_widjet import fade_widget
from main.utils import Close

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt, QTimer



class Menu_bddWindow(QWidget):
    def __init__(self, style_base_donné, connection, choix_bdd):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} - {VERSION}")
        self.resize(600, 400)
        self.style_base_donné = style_base_donné
        self.choix_bdd = choix_bdd
        self.connection = connection

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

        try:
            table_name = recuperer_tables(self.style_base_donné,self.connection, self.choix_bdd)
            self.ouvrir_gestion_table(table_name)

        except Exception as e:
            self.message_label.setText(f"Erreur lors de la récupération des tables : {e}")
            print(f"Erreur globale : {e}")

    def chercher_dans_bdd(self):
        self.message_label.setText("Recherche en développement...")

    def faire_une_requete_sql(self):
        self.hide()
        from main.page.differente_bdd.page_sql import SQL_Window
        self.sql_window = SQL_Window(
            self.style_base_donné,
            self.connection,
            self.choix_bdd
            )
        self.sql_window.show()
        fade_widget(self.sql_window, duration=500, fade_in=True)
        QTimer.singleShot(1000, self.deleteLater)

    def retour(self):
        self.hide()
        from main.page.menu_principal_bdd import Menu_Principal_Window
        self.main_window = Menu_Principal_Window(
            self.style_base_donné,
            self.connection,
            self.choix_bdd
            )
        self.main_window.show()
        fade_widget(self.main_window, duration=500, fade_in=True)
        QTimer.singleShot(1000, self.deleteLater)

    def ouvrir_gestion_table(self, table_name):
        self.hide()
        from main.page.gestion_table import GestionTableWindow
        self.gestion_table_window = GestionTableWindow(
            self.style_base_donné,
            self.connection,
            self.choix_bdd,
            table_name=table_name,
        )
        self.gestion_table_window.show()
        fade_widget(self.gestion_table_window, duration=500, fade_in=True)
        QTimer.singleShot(1000, self.deleteLater)

    def closeEvent(self, event):
        Close(self, event)