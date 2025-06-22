import sys
import os
from PyQt6.QtWidgets import QApplication

if getattr(sys, '_MEIPASS', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(sys.argv[0]))

sys.path.insert(0, base_path)

from main.page.selection_style_bdd import ChoixBDDWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = ChoixBDDWindow()
    fenetre.show()
    sys.exit(app.exec())
