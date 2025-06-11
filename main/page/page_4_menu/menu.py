import sys
from pathlib import Path
from settings import APP_NAME, VERSION

sys.path.append(str(Path(__file__).resolve().parent / "main"))
# on initialise toujours PyQt6 pour les nouvelles fenêtres
# c'est le moteur graphique de l'application
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt

class MenuWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} - v{VERSION}")
        self.resize(600, 400)

        layout = QVBoxLayout()

        self.welcome_label = QLabel(f"Bienvenue, {username} ! Vous êtes sur la page du menu.")
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.welcome_label)

        self.setLayout(layout)