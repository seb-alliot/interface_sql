def Close(widget, event):
    connection = widget.connection[0] if isinstance(widget.connection, tuple) else widget.connection
    try:
        changement = getattr(widget, "changement_de_page", False)
        if connection and not changement:
            try:
                connection.close()
                print("Connexion fermée proprement.")
            except Exception as e:
                print(f"Erreur lors de la fermeture de la connexion : {e}")
            finally:
                widget.connection = None
        else:
            if changement:
                print("Changement de page détecté, pas de fermeture de connexion.")
            elif widget.connection[1]:
                return ["Aucune connexion active , {widget.connection[1]}"]
    finally:
        event.accept()
