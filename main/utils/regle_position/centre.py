from PyQt6.QtWidgets import QApplication


def center_on_screen(self):
    screen = QApplication.primaryScreen()
    screen_geometry = screen.geometry()
    x = (screen_geometry.width() - self.width()) / 2
    y = (screen_geometry.height() - self.height()) / 2
    self.move(int(x), int(y))