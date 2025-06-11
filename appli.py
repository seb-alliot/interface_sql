import sys
import os
from PyQt6.QtWidgets import QApplication

base_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, base_path)

from main.page.page_1_verification import VerificationWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = VerificationWindow()
    fenetre.show()
    sys.exit(app.exec())
