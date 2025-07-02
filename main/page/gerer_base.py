import sys
import os
from dotenv import load_dotenv
from pathlib import Path
from settings import APP_NAME, VERSION
from main.utils.regles_visuelles.fad_widjet import fade_widget
from main.page.menu_principal_bdd import Menu_Principal_Window
from main.utils import Close
from main import center_on_screen
from main.utils.fonction_diverse.import_modul import importer_module_bdd

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

from PyQt6.QtWidgets import (
    QWidget,         # Classe de base pour toutes les fenêtres et widgets
    QVBoxLayout,     # Layout vertical pour organiser les widgets en colonne
    QHBoxLayout,     # Layout horizontal pour organiser les widgets en ligne
    QComboBox,       # Menu déroulant (liste de sélection)
    QStackedWidget,  # Conteneur qui affiche une seule "page" parmi plusieurs
    QLabel,          # Widget pour afficher du texte
    QLineEdit,       # Champ de saisie de texte (input)
    QPushButton,     # Bouton cliquable
    QApplication,    # Objet principal qui gère l’application
    QTextEdit,       # Widget pour afficher et éditer du texte multi-lignes
    QMessageBox,     # Boîte de dialogue pour afficher des messages
)
from PyQt6.QtCore import Qt, QTimer  # Qt pour les constantes, QTimer pour les temporisations
from PyQt6.QtCore import pyqtSignal  # Pour les signaux personnalisés
from .page_gestion_base.page_create import Creation_table_window


class Gerer_Base_Window(QWidget):
    affiche_sql = pyqtSignal(str)

    def __init__(self, module, style_base_donne, connection, choix_bdd):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} - v{VERSION}")
        self.resize(600, 400)
        center_on_screen(self)
        self.setFocus()

        self.style_base_donne = style_base_donne
        self.connection = connection
        self.choix_bdd = choix_bdd

        # Import dynamique du module selon style de base
        self.module = importer_module_bdd(self.style_base_donne)

        # Création unique de page_create avec connexion du signal
        self.page_create = Creation_table_window(
            module=self.module,
            style_base_donne=self.style_base_donne,
            connection=self.connection,
            choix_bdd=self.choix_bdd
        )
        self.page_create.affiche_sql.connect(self.afficher_requete_sql)

        self.page_modify = ModifyTableWidget(self.module)
        self.empty_page = QLabel("Choisissez une action")
        self.empty_page.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()

        self.label = QLabel("Gérer la base de données")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.combo = QComboBox()
        self.combo.addItems([
            "Sélectionnez une action",
            "Créer une table",
            "Modifier une table",
            "Supprimer une table",
            "Insérer des données",
            "Modifier des données",
            "Supprimer des données",
        ])
        layout.addWidget(self.combo)

        self.stack = QStackedWidget()
        self.stack.addWidget(self.empty_page)   # index 0
        self.stack.addWidget(self.page_create)  # index 1
        self.stack.addWidget(self.page_modify)  # index 2
        layout.addWidget(self.stack)

        self.combo.currentIndexChanged.connect(self.on_action_changed)
        self.stack.setCurrentIndex(0)

        # Zone d'affichage des requêtes SQL
        self.zone_affichage_sql = QTextEdit()
        self.zone_affichage_sql.setPlaceholderText("Affichage des requêtes SQL exécutées...")
        self.zone_affichage_sql.setReadOnly(True)
        self.zone_affichage_sql.setMinimumSize(400, 200)
        self.zone_affichage_sql.setMaximumSize(600, 300)
        self.zone_affichage_sql.setStyleSheet("""
            QTextEdit {
                background-color: black;
                border: 1px solid #cccccc;
                padding: 10px;
                font-family: monospace;
                font-size: 12px;
            }
        """)
        layout.addWidget(self.zone_affichage_sql)

        # Titre pour la zone d'affichage SQL
        self.titre_zone_sql = QLabel("Requêtes SQL exécutées :")
        self.titre_zone_sql.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.titre_zone_sql.setStyleSheet("font-size: 14px; font-weight: bold; color: black;")
        layout.addWidget(self.titre_zone_sql, alignment=Qt.AlignmentFlag.AlignCenter)

        # Bouton de retour
        self.retour_button = QPushButton("Retour")
        self.retour_button.setStyleSheet("font-size: 14px; color: white;")
        self.retour_button.setMinimumSize(200, 30)
        self.retour_button.setMaximumSize(300, 45)
        self.retour_button.clicked.connect(self.retour)
        layout.addWidget(self.retour_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)

    def afficher_requete_sql(self, requete: str):
        self.zone_affichage_sql.append(requete)

    def on_action_changed(self, index):
        if index == 0:
            self.stack.setCurrentIndex(0)
        elif index == 1:
            self.stack.setCurrentIndex(1)
        elif index == 2:
            self.stack.setCurrentIndex(2)
        elif index == 3:
            self.stack.setCurrentIndex(3)
        elif index == 4:
            self.stack.setCurrentIndex(4)
        elif index == 5:
            self.stack.setCurrentIndex(5)
        elif index == 6:
            self.stack.setCurrentIndex(6)

    def retour(self):
        self.hide()
        self.main_window = Menu_Principal_Window(
            self.style_base_donne,
            self.connection,
            self.choix_bdd)
        self.main_window.show()
        fade_widget(self.main_window, duration=500, fade_in=True)
        QTimer.singleShot(1000, self.deleteLater)

    def closeEvent(self, event):
        pass


class ModifyTableWidget(QWidget):
    def __init__(self, module):
        super().__init__()
        self.module = module
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Modification de table"))
        # Ici, tu peux récupérer les tables et afficher les options de modif
        self.setLayout(layout)
