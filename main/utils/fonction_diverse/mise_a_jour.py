import requests
import hashlib
import os
import settings
from PyQt6.QtCore import QThread, pyqtSignal

class VerifMajThread(QThread):
    """
    Thread de vérification et téléchargement automatique de mise à jour.

    Ce thread vérifie la version actuelle en ligne via un fichier JSON, compare avec la version locale,
    télécharge la nouvelle version si disponible, vérifie l'intégrité via SHA256,
    puis émet un signal pour lancer la nouvelle version.

    Signaux émis :
        maj_result(str message, str couleur) : pour informer de l'état d'avancement.
        maj_finie() : pour indiquer que la mise à jour a été téléchargée et est prête à être lancée.
    """

    maj_result = pyqtSignal(str, str)  # Message à afficher + couleur du texte
    maj_finie = pyqtSignal()           # Signal pour indiquer que la mise à jour est prête

    URL_JSON = "http://147.93.90.211/sql_by_itsuki/version.json"
    CHEMIN_EXE_LOCAL = "appli_by_itsuki.exe"

    def Mise_a_jour(self, url, chemin_local):
        """
        Télécharge un fichier depuis une URL et l'enregistre localement.

        Args:
            url (str): URL du fichier à télécharger.
            chemin_local (str): Chemin local où sauvegarder le fichier.
        """
        response = requests.get(url, stream=True)
        with open(chemin_local, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # Évite d'écrire des chunks vides
                    f.write(chunk)

    def get_sha256(self, filepath):
        """
        Calcule le hash SHA256 d'un fichier.

        Args:
            filepath (str): Chemin du fichier à hasher.

        Returns:
            str: Hash SHA256 en hexadécimal.
        """
        with open(filepath, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()

    def run(self, VERSION=settings.VERSION):
        """
        Point d'entrée du thread : vérifie la mise à jour, télécharge et valide le fichier.

        Args:
            VERSION (str): Version locale actuelle de l'application.
        """
        try:
            self.maj_result.emit("🔄 Vérification de mise à jour...", "white")

            # Récupérer les infos de version en ligne depuis le JSON
            response = requests.get(self.URL_JSON, timeout=10)
            data = response.json()

            version_en_ligne = data.get("version")
            url_exe = data.get("url")
            hash_exe = data.get("sha256")

            # Comparer versions
            if version_en_ligne > VERSION:
                self.maj_result.emit(f"🆕 Nouvelle version {version_en_ligne} disponible.", "blue")
                self.maj_result.emit("⬇️ Téléchargement en cours...", "cyan")

                # Télécharger le nouvel exécutable
                self.Mise_a_jour(url_exe, self.CHEMIN_EXE_LOCAL)

                # Vérifier l'intégrité du fichier téléchargé
                hash_local = self.get_sha256(self.CHEMIN_EXE_LOCAL)
                if hash_local.lower() == hash_exe.lower():
                    self.maj_result.emit("✅ Mise à jour téléchargée avec succès. Lancement de la nouvelle version...", "green")
                    self.maj_finie.emit()  # Signal pour lancer la nouvelle version
                else:
                    self.maj_result.emit("❌ Fichier corrompu, suppression du fichier.", "red")
                    os.remove(self.CHEMIN_EXE_LOCAL)
            else:
                self.maj_result.emit("👍 Aucune mise à jour disponible.", "green")

        except Exception as e:
            self.maj_result.emit(f"⚠️ Erreur lors de la vérification : {e}", "red")
