from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout
import sys

# Fenêtre principale
class Test_Visuel_Interface(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("2x2 boutons alignés horizontalement")
        self.resize(600, 400)

        # Création des boutons
        btn1 = QPushButton("Bouton 1")
        btn2 = QPushButton("Bouton 2")
        btn3 = QPushButton("Bouton 3")
        btn4 = QPushButton("Bouton 4")

        # Colonne de gauche (verticale)
        colonne_gauche = QVBoxLayout()
        colonne_gauche.addWidget(btn1)
        colonne_gauche.addWidget(btn2)

        # Colonne de droite (verticale)
        colonne_droite = QVBoxLayout()
        colonne_droite.addWidget(btn3)
        colonne_droite.addWidget(btn4)

        # Layout principal horizontal
        layout_principal = QHBoxLayout()
        layout_principal.addLayout(colonne_gauche)
        layout_principal.addLayout(colonne_droite)

        # Appliquer le layout à la fenêtre
        self.setLayout(layout_principal)

        # 🔁 Ordre de tabulation personnalisé : gauche → droite
        QWidget.setTabOrder(btn1, btn3)  # première ligne gauche à droite
        QWidget.setTabOrder(btn3, btn2)  # descente à la ligne gauche
        QWidget.setTabOrder(btn2, btn4)  # ligne 2 gauche à droite
        
# Lancement de l'application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = Test_Visuel_Interface()
    fenetre.show()
    sys.exit(app.exec())
