import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent / "main"))

from page.page_1_connection.code.connection_db import message_bienvenu, connect_to_database
from settings import APP_NAME, VERSION, DB_CONFIG, APP_SECRET
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
)
from PyQt6.QtCore import Qt

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} - v{VERSION}")
        self.resize(400, 250)

        layout = QVBoxLayout()

        self.input_pseudo = QLineEdit()
        self.input_pseudo.setPlaceholderText("Entrez votre prénom")
        layout.addWidget(self.input_pseudo)

        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.input_password.setPlaceholderText("Entrez votre mot de passe")
        layout.addWidget(self.input_password)

        self.bouton = QPushButton("Démarrer")
        self.bouton.clicked.connect(self.bouton_connection)
        layout.addWidget(self.bouton)

        self.message_info = QLabel("")
        self.message_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.message_info)

        self.setLayout(layout)

    def bouton_connection(self):
        nom = self.input_pseudo.text().strip()
        if not nom:
            self.message_info.setText("Veuillez entrer un identifiant.")
            return
        password = self.input_password.text().strip()
        if not password:
            self.message_info.setText("Veuillez entrer un mot de passe.")
            return

        if nom == DB_CONFIG['user'] and password == DB_CONFIG['password']:
            try:
                connection, error = connect_to_database()
                if connection:
                    self.message_info.setText(message_bienvenu(nom))
                    connection.close()
                else:
                    self.message_info.setText("Échec de la connexion à la base de données.")
            except Exception as e:
                self.message_info.setText("Identifiants incorrects.")
        else:
            self.message_info.setText("Identifiants incorrects.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = LoginWindow()
    fenetre.show()
    sys.exit(app.exec())
