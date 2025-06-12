from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer
from ..regle_position import center_on_screen

class TransitionWindow(QWidget):
    def __init__(self, username, on_transition_done):
        super().__init__()
        self.setWindowTitle("Transition")
        self.resize(600, 400)
        center_on_screen(self)  # centrage du message sur l'écran

        layout = QVBoxLayout()
        label = QLabel(f"Bienvenue {username} ! Chargement du menu...")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        self.setLayout(layout)

        # Attendre 1.5 secondes puis appeler la fonction de fin
        QTimer.singleShot(1500, on_transition_done)