from PyQt6.QtCore import QPropertyAnimation
from PyQt6.QtWidgets import QGraphicsOpacityEffect

def fade_widget(widget, duration=300, fade_in=True, finished_callback=None):
    effect = QGraphicsOpacityEffect()
    widget.setGraphicsEffect(effect)

    animation = QPropertyAnimation(effect, b"opacity", widget)
    animation.setDuration(duration)
    animation.setStartValue(0.0 if fade_in else 1.0)
    animation.setEndValue(1.0 if fade_in else 0.0)

    # important : garder la référence sur l'objet parent (le widget)
    widget._fade_animation = animation

    if finished_callback:
        animation.finished.connect(finished_callback)

    animation.start()
