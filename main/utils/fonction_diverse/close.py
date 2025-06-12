def Close(*arguments):
    for arg in arguments:
        try:
            arg.close()
        except Exception as e:
            print(f"Erreur lors de la fermeture de {arg}: {e}")
    return None