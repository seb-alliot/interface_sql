import requests
import hashlib
import os
import sys
import zipfile
import shutil
from PyQt6.QtCore import QThread, pyqtSignal
import settings

class VerifMajThread(QThread):
    maj_result = pyqtSignal(str, str)
    maj_finie = pyqtSignal()

    url_json = "https://byitsuki.com/media/application/appli_sql_version.json"
    CHEMIN_ZIP_LOCAL = "update_temp.zip"
    DOSSIER_TEMP = "update_temp_dir"
    DOSSIER_FINAL = "."  # Dossier courant

    def Mise_a_jour(self, url, chemin_local):
        try:
            response = requests.get(url, stream=True)
            with open(chemin_local, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
        except Exception as e:
            self.maj_result.emit(f"❌ Erreur téléchargement : {e}", "red")
            raise

    def get_sha256(self, filepath):
        try:
            with open(filepath, "rb") as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception as e:
            self.maj_result.emit(f"❌ Erreur calcul hash : {e}", "red")
            raise

    def lire_version_externe(self, url_json):
        try:
            response = requests.get(url_json, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.maj_result.emit(f"❌ Erreur lecture version distante : {e}", "red")
            raise

    def mettre_a_jour_version_env(self, fichier_env, nouvelle_version):
        try:
            lignes_modifiees = []
            with open(fichier_env, 'r', encoding='utf-8') as f:
                lignes = f.readlines()
                for ligne in lignes:
                    if ligne.strip().startswith("APP_VERSION="):
                        lignes_modifiees.append(f"APP_VERSION={nouvelle_version}\n")
                    else:
                        lignes_modifiees.append(ligne)

            with open(fichier_env, 'w', encoding='utf-8') as f:
                f.writelines(lignes_modifiees)
        except Exception as e:
            self.maj_result.emit(f"❌ Erreur mise à jour .env : {e}", "red")
            raise

    def remplacer_dossier(self, source_dir, target_dir):
        try:
            if os.path.exists(target_dir):
                for fichier in os.listdir(source_dir):
                    if fichier.lower() == "launcher.exe":
                        continue  # 🔁 On ignore le launcher en cours d'exécution

                    src = os.path.join(source_dir, fichier)
                    dst = os.path.join(target_dir, fichier)

                    # Supprimer l'ancienne version si elle existe
                    if os.path.exists(dst):
                        if os.path.isfile(dst):
                            os.remove(dst)
                        elif os.path.isdir(dst):
                            shutil.rmtree(dst)

                    # Copier la nouvelle version
                    if os.path.isfile(src):
                        shutil.copy2(src, dst)
                    elif os.path.isdir(src):
                        shutil.copytree(src, dst)
        except Exception as e:
            self.maj_result.emit(f"❌ Erreur remplacement des fichiers : {e}", "red")
            raise


    def run(self, VERSION=settings.VERSION):
        try:
            self.maj_result.emit("🔄 Vérification de la version distante...", "white")
            data = self.lire_version_externe(self.url_json)

            version_en_ligne = data.get("version")
            url_zip = data.get("url")
            hash_exe = data.get("sha256")

            if version_en_ligne > VERSION:
                self.maj_result.emit(f"🆕 Nouvelle version {version_en_ligne} disponible.", "blue")
                self.maj_result.emit("⬇️ Téléchargement du ZIP de mise à jour...", "cyan")
                self.Mise_a_jour(url_zip, self.CHEMIN_ZIP_LOCAL)

                self.maj_result.emit("📦 Extraction du contenu...", "cyan")
                try:
                    if os.path.exists(self.DOSSIER_TEMP):
                        shutil.rmtree(self.DOSSIER_TEMP)
                    with zipfile.ZipFile(self.CHEMIN_ZIP_LOCAL, 'r') as zipf:
                        zipf.extractall(self.DOSSIER_TEMP)
                        print(f"Contenu extrait dans {self.DOSSIER_TEMP}")
                except Exception as e:
                    self.maj_result.emit(f"❌ Erreur extraction ZIP : {e}", "red")
                    raise

                exe_temp_path = os.path.join(self.DOSSIER_TEMP, "appli_by_itsuki.exe")
                hash_local_exe = self.get_sha256(exe_temp_path)
                if hash_local_exe.lower() != hash_exe.lower():
                    self.maj_result.emit("❌ Exécutable corrompu, suppression...", "red")
                    try:
                        os.remove(self.CHEMIN_ZIP_LOCAL)
                        shutil.rmtree(self.DOSSIER_TEMP)
                    except Exception as e:
                        self.maj_result.emit(f"⚠️ Erreur nettoyage : {e}", "yellow")
                    return

                chemin_env_temp = os.path.join(self.DOSSIER_TEMP, ".env")
                if os.path.exists(chemin_env_temp):
                    self.mettre_a_jour_version_env(chemin_env_temp, VERSION)
                    print(f" content de {chemin_env_temp} mis à jour avec la version {VERSION}")
                    print(f"Version mise à jour dans {chemin_env_temp}, sa merde ici !")

                self.maj_result.emit("📂 Installation de la mise à jour...", "cyan")
                print(f"Remplacement du dossier {self.DOSSIER_FINAL} par {self.DOSSIER_TEMP}")
                self.remplacer_dossier(self.DOSSIER_TEMP, self.DOSSIER_FINAL)
                print("Dossier remplacé avec succès.")

                self.maj_result.emit("✅ Mise à jour terminée avec succès.", "green")
                self.maj_finie.emit()

                try:
                    os.remove(self.CHEMIN_ZIP_LOCAL)
                    if os.path.exists(self.DOSSIER_TEMP):
                        shutil.rmtree(self.DOSSIER_TEMP)
                except Exception as e:
                    self.maj_result.emit(f"⚠️ Erreur nettoyage final : {e}", "yellow")

            else:
                self.maj_result.emit("👍 Aucune mise à jour disponible.", "green")
                self.maj_finie.emit()

        except Exception as e:
            self.maj_result.emit(f"⚠️ Erreur mise à jour : {e}", "red")
            print("Erreur mise à jour :", e)
