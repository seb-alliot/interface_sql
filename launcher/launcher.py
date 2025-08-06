import sys
import os
import subprocess
import tempfile
from dotenv import load_dotenv
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton
base_path = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)

load_dotenv(dotenv_path=os.path.join(base_path, '.env'))
# Détection du chemin de base en mode .py ou .exe (PyInstaller)
BASE_DIR = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(__file__)
RACINE = os.path.abspath(os.path.join(BASE_DIR, '..'))

# Ajout au sys.path
if RACINE not in sys.path:
    sys.path.insert(0, RACINE)
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Import des paramètres
import settings
from launcher.utils.mise_a_jour import VerifMajThread

class LauncherWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(500, 200)
        self.setWindowTitle(f"{settings.APP_NAME} - {settings.VERSION}")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_status = QLabel("Vérification des mises à jour...")
        self.label_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label_status)

        self.button_lancer = QPushButton("Lancer l'application")
        self.button_lancer.setEnabled(False)
        self.button_lancer.clicked.connect(self.lancer_appli)
        layout.addWidget(self.button_lancer)

        self.setLayout(layout)

        self.thread_maj = VerifMajThread()
        self.thread_maj.maj_result.connect(self.update_label)
        self.thread_maj.maj_finie.connect(self.lancer_remplacement_si_necessaire)
        self.thread_maj.start()

    def update_label(self, message, color):
        self.label_status.setText(message)
        self.label_status.setStyleSheet(f"color: {color}; font-size: 14px; padding: 10px;")

    def lancer_remplacement_si_necessaire(self):
        exe_actuel = os.path.join(BASE_DIR, "appli_by_itsuki.exe")
        exe_nouveau = os.path.join(BASE_DIR, "appli_by_itsuki_new.exe")

        if os.path.exists(exe_nouveau):
            self.label_status.setText("Remplacement de la version...")
            batch_script = f"""@echo off
            :loop
            tasklist /FI "IMAGENAME eq {os.path.basename(exe_actuel)}" | find /I "{os.path.basename(exe_actuel)}" >nul
            if not errorlevel 1 (
                timeout /t 1 /nobreak >nul
                goto loop
            )
            move /Y "{exe_nouveau}" "{exe_actuel}"
            start "" "{exe_actuel}"
            del "%~f0"
            """
            bat_path = os.path.join(tempfile.gettempdir(), "maj_replace.bat")
            with open(bat_path, "w", encoding="utf-8") as f:
                f.write(batch_script)

            subprocess.Popen([bat_path], shell=True)
            self.close()
        else:
            self.label_status.setText("Application à jour.")
            self.button_lancer.setEnabled(True)
            self.button_lancer.setText("Lancer l'application")
            self.lancer_appli()
        self.thread_maj.terminate()

    def lancer_appli(self):
        load_dotenv(override=True)
        exe_path = os.path.join(BASE_DIR, "appli_by_itsuki.exe")
        if os.path.exists(exe_path):
            subprocess.Popen([exe_path, "--from-launcher"])
            self.close()
        else:
            self.update_label("Fichier introuvable : appli_by_itsuki.exe", "red")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LauncherWindow()
    window.show()
    sys.exit(app.exec())