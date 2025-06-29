def save_bdd_config(DB_CONFIG, env_path=".env"):

    import os

    if not os.path.exists(env_path):
        raise FileNotFoundError(f"Le fichier {env_path} n'existe pas.")

    with open(env_path, 'r+') as f:
        lignes_lues = f.readlines()
        f.seek(0)
        nouvelles_lignes = []

        clef_entree = {clef: False for clef in DB_CONFIG.keys()}

        for ligne in lignes_lues:
            # Ignorer lignes vides ou commentaires
            if ligne.strip() == "" or ligne.lstrip().startswith("#"):
                nouvelles_lignes.append(ligne)
                continue

            clef = ligne.split('=')[0].strip()
            if clef in DB_CONFIG:
                nouvelles_lignes.append(f"{clef}={DB_CONFIG[clef]}\n")
                clef_entree[clef] = True
            else:
                nouvelles_lignes.append(ligne)

        for clef, valeur in DB_CONFIG.items():
            if not clef_entree[clef]:
                nouvelles_lignes.append(f"{clef}={valeur}\n")

        f.writelines(nouvelles_lignes)
        f.truncate()