import sys
from pathlib import Path
from settings import APP_NAME, VERSION

project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(Path(__file__).resolve().parent / "main"))

from main.utils.fonction_diverse.recharge_env import recharger_env
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton
from PyQt6.QtCore import Qt, QTimer
from main.utils.fonction_diverse import importer_module_bdd
from main.utils import Close


class Menu_Principal_Window(QWidget):
    def __init__(self, style_base_donne, connection, choix_bdd=None):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} - {VERSION}")
        self.resize(600, 400)
        self.setFocus()
        self.style_base_donne = style_base_donne
        self.connection = connection
        self.module = importer_module_bdd(self.style_base_donne)
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
        connection = self.connection[0]
        if connection:
            connection.close()
        from main.page.selection_style_bdd import ChoixBDDWindow
        self.main_window = ChoixBDDWindow(self.connection)
        self.main_window.show()
        from main.utils.regles_visuelles.fad_widjet import fade_widget
        fade_widget(self.main_window, duration=500, fade_in=True)
        QTimer.singleShot(1000, self.deleteLater)

    def list_bdd(self):
        if not self.connection:
            return ["Aucune connexion active"]

        if self.style_base_donne == "MongoDB":
            try:
                query_module = self.module.import_query_module("voir_base")
                return query_module.voir_base(self.connection[0])
            except Exception as e:
                return [f"Erreur MongoDB : {str(e)}"]

        connection = self.connection[0]
        if not connection:
            return ["Connexion invalide"]
        cursor = connection.cursor()

        try:
            query_module = self.module.import_query_module("voir_base")
            if query_module and hasattr(query_module, "voir_base"):
                cursor.execute(query_module.voir_base())
                return [bdd[0] for bdd in cursor.fetchall()]
            else:
                return ["Module query 'voir_base' non disponible"]
        except Exception as e:
            return [f"Erreur SQL : {str(e)}"]


    def connection_bdd(self):
        recharger_env()
        choix_bdd = self.choix_bdd_combo.currentText()
        nouvelle_connection = None
        if not self.connection:
            self.label_bdd.setText("Aucune connexion active")
            return

        try:
            if self.style_base_donne == "MongoDB":
                nouvelle_connection = self.connection
            else:
                # Récupérer config avec la base choisie
                db_config = self.module.config(dbname=choix_bdd)
                # Connect retourne juste l'objet connection (pas de tuple)
                nouvelle_connection = self.module.connect(db_config)
                if not nouvelle_connection:
                    self.label_bdd.setText("Erreur de connexion (connection vide)")
                    return

            self.connection = nouvelle_connection

            self.menu_bdd()
        except Exception as e:
            self.label_bdd.setText(f"Erreur de connexion : {str(e)}")

    def menu_bdd(self):
        self.hide()
        from main.page.choix_bdd import Menu_bddWindow
        self.main_window = Menu_bddWindow(
            style_base_donne=self.style_base_donne,
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
            self.style_base_donne,
            connection=self.connection,
        )
        self.main_window.show()
        from main.utils.regles_visuelles.fad_widjet import fade_widget
        fade_widget(self.main_window, duration=500, fade_in=True)
        QTimer.singleShot(1000, self.deleteLater)

    def closeEvent(self, event):
        Close(self, event)
