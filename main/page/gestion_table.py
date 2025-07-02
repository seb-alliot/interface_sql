import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(Path(__file__).resolve().parent / "main"))


from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QComboBox,
    QPushButton, QHBoxLayout, QMessageBox
)
from PyQt6.QtCore import Qt
from settings import APP_NAME, VERSION
from main.utils import Close, fermer_et_transfere
from main.utils.fonction_diverse import importer_module_bdd
from main.utils.gestion_bdd.affichage_table import recuperer_tables


class GestionTableWindow(QWidget):
    STYLE_BOUTON_BASE = """
        QPushButton {
            font-size: 14px;
            padding: 5px;
            background-color: none;
        }
    """

    STYLE_BOUTON_SELECTIONNE = """
        QPushButton {
            font-size: 14px;
            padding: 5px;
            background-color: lightblue;
        }
        QPushButton:hover {
            background-color: #a8d8ff;
        }
    """

    def __init__(self, style_base_donne, connection, choix_bdd, table_name):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} - {VERSION}")
        self.resize(600, 400)
        self.setFocus()
        self.style_base_donne = style_base_donne
        self.choix_bdd = choix_bdd
        self.table_name = table_name
        self.connection = connection

        # Import dynamique du module selon style_base_donne
        self.module = importer_module_bdd(self.style_base_donne)

        vertical_layout = QVBoxLayout()

        self.message_label = QLabel("Que voulez-vous faire ? :")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setStyleSheet("font-size: 14px; color: orange;")
        vertical_layout.addWidget(self.message_label)

        self.select_table_name = QLabel()
        self.select_table_name.setMinimumSize(200, 30)
        self.select_table_name.setMaximumSize(300, 45)
        self.select_table_name.setStyleSheet("font-size: 14px; padding: 5px;")
        self.select_table_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.select_table_name.hide()
        vertical_layout.addWidget(self.select_table_name)

        self.combo = QComboBox()
        self.combo.setMinimumSize(200, 30)
        self.combo.setMaximumSize(300, 45)
        self.combo.setStyleSheet("font-size: 14px; padding: 5px;")
        self.option1 = "Sélectionner une table"
        self.combo.addItem(self.option1)
        self.combo.addItems(self.table_name)
        self.combo.currentTextChanged.connect(self.update_table_name)
        vertical_layout.addWidget(self.combo, alignment=Qt.AlignmentFlag.AlignCenter)

        # === Boutons d'action ===
        self.button_contenu_table = QPushButton("Contenu de la table")
        self.button_chercher_dans_table = QPushButton("Modifier la table")
        self.button_faire_une_requete_sql = QPushButton("Faire une requête SQL")

        self.buttons = [
            self.button_contenu_table,
            self.button_chercher_dans_table,
            self.button_faire_une_requete_sql,
        ]

        horizontal_layout = QHBoxLayout()
        for button in self.buttons:
            button.setMinimumSize(200, 30)
            button.setMaximumSize(300, 45)
            button.setStyleSheet(self.STYLE_BOUTON_BASE)
            button.clicked.connect(lambda _, b=button: self.selectionner_action(b))
            horizontal_layout.addWidget(button)

        vertical_layout.addLayout(horizontal_layout)

        # === Valider / Retour ===
        self.button_validation_action = QPushButton("Valider")
        self.button_validation_action.clicked.connect(self.validation_action)

        self.retour_button = QPushButton("Retour")
        self.retour_button.clicked.connect(self.retour)

        for button in [self.button_validation_action, self.retour_button]:
            button.setMinimumSize(200, 30)
            button.setMaximumSize(300, 45)
            button.setStyleSheet("font-size: 14px; padding: 5px;")

        vertical_layout.addWidget(self.button_validation_action, alignment=Qt.AlignmentFlag.AlignCenter)
        vertical_layout.addWidget(self.retour_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(vertical_layout)

    def update_table_name(self, text):
        if text != self.option1:
            self.select_table_name.hide()

    def selectionner_action(self, bouton_selectionne):
        for button in self.buttons:
            if button == bouton_selectionne:
                button.setStyleSheet(self.STYLE_BOUTON_SELECTIONNE)
                self.action_selectionnee = button
            else:
                button.setStyleSheet(self.STYLE_BOUTON_BASE)

    def validation_action(self):
        table_selectionnee = self.combo.currentText()

        if table_selectionnee == self.option1:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une table.")
            return

        if not hasattr(self, "action_selectionnee") or not self.action_selectionnee:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner une action.")
            return

        if self.action_selectionnee == self.button_contenu_table:
            self.afficher_table()
        elif self.action_selectionnee == self.button_chercher_dans_table:
            self.modifier_table_sql()
        elif self.action_selectionnee == self.button_faire_une_requete_sql:
            self.afficher_console_sql()

    def retour(self):
        fermer_et_transfere(self)
        from main.page.choix_bdd import Menu_bddWindow
        self.menu_bdd_window = Menu_bddWindow(
            self.style_base_donne,
            self.connection,
            self.choix_bdd,
        )
        self.menu_bdd_window.show()

    def afficher_table(self):
        fermer_et_transfere(self)
        from main.page.requete_sql.afficher_table_sql import Afficher_Table_SQL_Window
        self.requete_sql_window = Afficher_Table_SQL_Window(
            self.style_base_donne,
            self.connection,
            self.choix_bdd,
            table_name=[self.combo.currentText()],
        )
        self.requete_sql_window.show()

    def modifier_table_sql(self):
        fermer_et_transfere(self)
        from main.page.requete_sql.modifier_table import Modifier_Table_Window
        self.requete_sql_window = Modifier_Table_Window(self.choix_bdd, [self.combo.currentText()])
        self.requete_sql_window.show()

    def afficher_console_sql(self):
        fermer_et_transfere(self)
        from main.page.requete_sql_sur_table import Requete_sql_sur_table
        self.requete_sql_window = Requete_sql_sur_table(
            self.style_base_donne,
            self.connection,
            self.choix_bdd,
            table_name=[self.combo.currentText()],
        )
        self.requete_sql_window.show()

    def closeEvent(self, event):
        Close(self, event)
