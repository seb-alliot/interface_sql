def Close(widget, event):
    try:
        changement = getattr(widget, "changement_de_page", False)
        if widget.connection and not changement:
            try:
                widget.connection.close()
                print("Connexion fermée proprement.")
            except Exception as e:
                print(f"Erreur lors de la fermeture de la connexion : {e}")
            finally:
                widget.connection = None
        else:
            print("Aucune connexion à fermer (changement de page ou pas de connexion).")
    finally:
        event.accept()

