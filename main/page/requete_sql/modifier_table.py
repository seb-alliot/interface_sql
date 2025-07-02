import sys
from pathlib import Path
from dotenv import load_dotenv

# Gestion du chemin
project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

from settings import APP_NAME, VERSION
from main import center_on_screen
from main.utils import Close
from main.utils.fonction_diverse import importer_module_bdd
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt


class Modifier_Table_Window(QWidget):
    def __init__(self, style_base_donne, connection, table_name):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} - {VERSION}")
        self.resize(700, 450)
        center_on_screen(self)

        self.style_base_donne = style_base_donne
        self.connection = connection
        self.table_name = table_name[0] if isinstance(table_name, list) else table_name

        self.module = importer_module_bdd(self.style_base_donne)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title_label = QLabel(f"Modification de la table : {self.table_name}")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: black;")
        layout.addWidget(self.title_label)

        self.message_label = QLabel("")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setStyleSheet("font-size: 14px; color: orange;")
        layout.addWidget(self.message_label)

        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)

        self.retour_button = QPushButton("Retour")
        self.retour_button.clicked.connect(self.close)
        layout.addWidget(self.retour_button, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(layout)



    def closeEvent(self, event):
        Close(self, event)
