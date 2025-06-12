from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
import sys
import time

def fade_widget(widget, duration=1000, fade_in=True, finished_callback=None):
    from PyQt6.QtCore import QPropertyAnimation
    from PyQt6.QtWidgets import QGraphicsOpacityEffect

    opacity_effect = QGraphicsOpacityEffect(widget)
    widget.setGraphicsEffect(opacity_effect)

    animation = QPropertyAnimation(opacity_effect, b"opacity")
    animation.setDuration(duration)
    if fade_in:
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
    else:
        animation.setStartValue(1.0)
        animation.setEndValue(0.0)

    animation.finished.connect(lambda: print("Animation terminée") or (finished_callback() if finished_callback else None))
    animation.start()
    widget._fade_animation = animation
    print("Animation démarrée")

class TestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test fade")
        self.resize(300, 200)
        layout = QVBoxLayout()
        self.label = QLabel("Salut")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        self.btn = QPushButton("Fade out")
        self.btn.clicked.connect(self.fade_out)
        layout.addWidget(self.btn)
        self.setLayout(layout)

    def fade_out(self):
        fade_widget(self, duration=1000, fade_in=False, finished_callback=self.fade_in)

    def fade_in(self):
        print("Fade out terminé, lancement fade in")
        fade_widget(self, duration=1000, fade_in=True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = TestWindow()
    w.show()
    sys.exit(app.exec())
