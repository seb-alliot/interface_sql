import sys
from pathlib import Path
from settings import APP_NAME, VERSION , MAJ_DB_CONFIG
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.append(str(Path(__file__).resolve().parent / "main"))

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QComboBox
)
from PyQt6.QtCore import Qt
from main.page.page_1_verification.code.connection_db import connect_to_database

class MenuWindow(QWidget):
    def __init__(self, username=None):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} - {VERSION}")
        self.resize(600, 400)
        self.setFocus()


        layout = QVBoxLayout()

        self.Menu_label = QLabel("Menu principal")
        self.Menu_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.Menu_label)

        self.label_langue = QLabel("Choisissez un langage de base :")
        layout.addWidget(self.label_langue)

        self.select_langage = QComboBox()
        self.select_langage.addItems(["Postsql"])  # à compléter plus tard
        self.select_langage.setMinimumWidth(200)
        self.select_langage.setMaximumWidth(300)
        self.select_langage.setMinimumHeight(30)
        self.select_langage.setMaximumHeight(45)
        self.select_langage.setStyleSheet("font-size: 14px; padding: 5px;")
        layout.addWidget(self.select_langage)

        self.label_bdd = QLabel("Choisissez une base de donnée :")
        layout.addWidget(self.label_bdd)

        self.select_bdd = QComboBox()
        self.select_bdd.addItems(self.list_bdd())
        self.select_bdd.setMinimumWidth(200)
        self.select_bdd.setMaximumWidth(300)
        self.select_bdd.setMinimumHeight(30)
        self.select_bdd.setMaximumHeight(45)
        self.select_bdd.setStyleSheet("font-size: 14px; padding: 5px;")
        layout.addWidget(self.select_bdd)

        self.setLayout(layout)

    def list_bdd(self):
        DB_CONFIG = MAJ_DB_CONFIG()
        connection_bdd, erreur = connect_to_database(DB_CONFIG)

        if connection_bdd is None or not connection_bdd:
            return ["Aucune base de données disponible"]

        if isinstance(connection_bdd, str):
            return [connection_bdd]

        try:
            cursor = connection_bdd.cursor()
            cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
            bdd_list = [bdd[0] for bdd in cursor.fetchall()]
            return bdd_list
        except Exception as e:
            return ["Erreur lors de la récupération des bases de données"]
        finally:
            if cursor:
                cursor.close()
            if connection_bdd:
                connection_bdd.close()

if __name__ == "__main__":
    app = QApplication([])
    fenetre = MenuWindow()
    fenetre.show()
    app.exec()
