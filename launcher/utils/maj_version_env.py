
import os

def maj_app_version_env(self, chemin_env, nouvelle_version):
    if not os.path.exists(chemin_env):
        return False
    try:
        lines = []
        with open(chemin_env, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        with open(chemin_env, 'w', encoding='utf-8') as f:
            modif = False
            for line in lines:
                if line.strip().startswith("APP_VERSION"):
                    f.write(f"APP_VERSION = {nouvelle_version}\n")
                    modif = True
                else:
                    f.write(line)
            # Si la ligne n'existait pas, on l'ajoute à la fin
            if not modif:
                f.write(f"\nAPP_VERSION = {nouvelle_version}\n")
        return True
    except Exception as e:
        print("Erreur mise à jour APP_VERSION dans .env :", e)
        return False
