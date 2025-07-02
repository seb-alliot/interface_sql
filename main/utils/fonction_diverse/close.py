def Close(widget, event):
    connection = widget.connection[0] if isinstance(widget.connection, tuple) else widget.connection
    try:
        changement = getattr(widget, "changement_de_page", False)
        if connection and not changement:
            try:
                connection.close()
            except Exception as e:
                return f"Erreur lors de la fermeture de la connexion : {e}"
            finally:
                widget.connection = None
        else:
            if changement:
                return ["Changement de page en cours, fermeture de la connexion..."]
            elif widget.connection[1]:
                return ["Aucune connexion active , {widget.connection[1]}"]
    finally:
        event.accept()
