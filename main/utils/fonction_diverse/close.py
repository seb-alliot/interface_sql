def Close(*args):
    for arg in args:
        try:
            arg.close()
        except Exception as e:
            print(f"Erreur lors de la fermeture de {arg}: {e}")
    return None