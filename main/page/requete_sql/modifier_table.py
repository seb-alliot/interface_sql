import sys
from pathlib import Path
from dotenv import load_dotenv
project_root = Path(__file__).resolve().parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))
# --- Fin de la correction ---

from main.utils.module.maria_db import connect_to_maria_database
from main.utils.module.postgres import connect_to_postgresql_database
from main import center_on_screen
from main.utils.regles_visuelles.fad_widjet import fade_widget
from main.page.menu_principal_bdd import Menu_Principal_Window
from main.utils.fonction_diverse.recharge_env import recharger_env
from main.utils import Close

from settings import APP_NAME, VERSION
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
)
from PyQt6.QtCore import Qt



class Modifier_Table_Window(QWidget):
    def __init__(self, style_base_donné, connection, table_name):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} - {VERSION}")
        self.resize(600, 400)
        center_on_screen(self)

        self.style_base_donné = style_base_donné
        self.connection = connection
        self.table_name = table_name
        self.setFocus()



    def closeEvent(self, event):
        Close(self, event)