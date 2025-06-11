from PyQt6.QtCore import QPropertyAnimation
from PyQt6.QtWidgets import QGraphicsOpacityEffect

def fade_widget(widget, duration=300, fade_in=True, finished_callback=None):
    """
    Anime un effet fondu sur un widget.

    Args:
        widget: Le widget PyQt6 à animer.
        duration: Durée de l'animation en millisecondes.
        fade_in: True pour fade in (apparition), False pour fade out (disparition).
        finished_callback: fonction à appeler à la fin de l'animation (optionnel).
    """
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

    if finished_callback:
        animation.finished.connect(finished_callback)

    animation.start()
    # Pour garder une référence sinon l'animation est détruite immédiatement
    widget._fade_animation = animation
