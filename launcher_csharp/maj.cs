using System;
using System.IO;
using System.Net.Http;
using System.Security.Cryptography;
using System.Text.Json;
using System.IO.Compression;
using System.Threading.Tasks;

namespace LauncherApp
{
    public class Mise_a_jour
    {
        public event Action<string, string>? OnStatusUpdate;
        public event Action? OnUpdateFinished;

        private readonly string urlJson = "https://byitsuki.com/media/application/appli_sql_version.json";
        private readonly string zipLocalPath;
        private readonly string tempDir = "update_temp_dir";
        private readonly string finalDir;
        private readonly string exeActuel;
        private readonly string exeNouveau;
        private readonly HttpClient httpClient = new();

        public Mise_a_jour(string baseDir, string exeActuel, string exeNouveau)
        {
            this.zipLocalPath = Path.Combine(baseDir, "update_temp.zip");
            this.finalDir = baseDir;
            this.exeActuel = exeActuel;
            this.exeNouveau = exeNouveau;
        }

        public async Task RunAsync(string currentVersion)
        {
            try
            {
                RaiseStatus("🔄 Vérification de la version distante...", "white");

                var data = await LireVersionExterneAsync();

                string versionEnLigne = data.version;
                string urlZip = data.url;
                string hashExe = data.sha256;

                if (ComparerVersions(versionEnLigne, currentVersion) > 0)
                {
                    RaiseStatus($"🆕 Nouvelle version {versionEnLigne} disponible.", "blue");
                    RaiseStatus("⬇️ Téléchargement du ZIP de mise à jour...", "cyan");

                    await TelechargerAsync(urlZip, zipLocalPath);

                    RaiseStatus("📦 Extraction du contenu...", "cyan");
                    ExtraireZip(zipLocalPath, tempDir);

                    string exeTempPath = Path.Combine(tempDir, "appli_by_itsuki.exe");
                    string hashLocalExe = CalculerSha256(exeTempPath);
                    if (!string.Equals(hashLocalExe, hashExe, StringComparison.OrdinalIgnoreCase))
                    {
                        RaiseStatus("Exécutable corrompu, suppression...", "red");
                        NettoyerFichiers();
                        return;
                    }

                    string cheminEnvTemp = Path.Combine(tempDir, ".env");
                    if (File.Exists(cheminEnvTemp))
                    {
                        MettreAJourVersionEnv(cheminEnvTemp, versionEnLigne);
                    }

                    RaiseStatus("📂 Installation de la mise à jour...", "cyan");
                    RemplacerDossier(tempDir, finalDir);
                    RaiseStatus("✅ Mise à jour terminée avec succès.", "green");

                    NettoyerFichiers();

                    OnUpdateFinished?.Invoke();
                }
                else
                {
                    RaiseStatus("👍 Aucune mise à jour disponible.", "green");
                    OnUpdateFinished?.Invoke();
                }
            }
            catch (Exception ex)
            {
                RaiseStatus($"⚠️ Erreur mise à jour : {ex.Message}", "red");
            }
        }

        private void RaiseStatus(string msg, string color)
            => OnStatusUpdate?.Invoke(msg, color);

        private async Task<(string version, string url, string sha256)> LireVersionExterneAsync()
        {
            var response = await httpClient.GetStringAsync(urlJson);
            using var doc = JsonDocument.Parse(response);
            var root = doc.RootElement;

            string version = root.GetProperty("version").GetString() ?? "";
            string url = root.GetProperty("url").GetString() ?? "";
            string sha256 = root.GetProperty("sha256").GetString() ?? "";

            return (version, url, sha256);
        }

        private async Task TelechargerAsync(string url, string cheminLocal)
        {
            using var response = await httpClient.GetAsync(url);
            response.EnsureSuccessStatusCode();

            using var fs = new FileStream(cheminLocal, FileMode.Create);
            await response.Content.CopyToAsync(fs);
        }

        private void ExtraireZip(string cheminZip, string dossierExtraction)
        {
            if (Directory.Exists(dossierExtraction))
                Directory.Delete(dossierExtraction, true);

            ZipFile.ExtractToDirectory(cheminZip, dossierExtraction);
        }

        private string CalculerSha256(string filepath)
        {
            using var stream = File.OpenRead(filepath);
            using var sha256 = SHA256.Create();
            byte[] hash = sha256.ComputeHash(stream);
            return BitConverter.ToString(hash).Replace("-", "").ToLowerInvariant();
        }

        private void MettreAJourVersionEnv(string cheminEnv, string nouvelleVersion)
        {
            var lignes = File.ReadAllLines(cheminEnv);
            bool modifie = false;

            for (int i = 0; i < lignes.Length; i++)
            {
                if (lignes[i].TrimStart().StartsWith("APP_VERSION="))
                {
                    lignes[i] = $"APP_VERSION={nouvelleVersion}";
                    modifie = true;
                }
            }
            if (!modifie)
            {
                using var sw = File.AppendText(cheminEnv);
                sw.WriteLine($"APP_VERSION={nouvelleVersion}");
            }
            else
            {
                File.WriteAllLines(cheminEnv, lignes);
            }
        }

        private void RemplacerDossier(string sourceDir, string targetDir)
        {
            foreach (var fichier in Directory.GetFileSystemEntries(sourceDir))
            {
                var nomFichier = Path.GetFileName(fichier);
                if (string.Equals(nomFichier, "launcher.exe", StringComparison.OrdinalIgnoreCase))
                    continue; // Ignorer launcher en cours

                var dest = Path.Combine(targetDir, nomFichier);

                if (File.Exists(dest)) File.Delete(dest);
                else if (Directory.Exists(dest)) Directory.Delete(dest, true);

                if (File.Exists(fichier))
                    File.Copy(fichier, dest);
                else if (Directory.Exists(fichier))
                    CopierDossierRecursif(fichier, dest);
            }
        }

        private void CopierDossierRecursif(string source, string destination)
        {
            Directory.CreateDirectory(destination);
            foreach (var dir in Directory.GetDirectories(source, "*", SearchOption.AllDirectories))
            {
                Directory.CreateDirectory(dir.Replace(source, destination));
            }
            foreach (var file in Directory.GetFiles(source, "*", SearchOption.AllDirectories))
            {
                File.Copy(file, file.Replace(source, destination));
            }
        }

        private void NettoyerFichiers()
        {
            try
            {
                if (File.Exists(zipLocalPath)) File.Delete(zipLocalPath);
                if (Directory.Exists(tempDir)) Directory.Delete(tempDir, true);
            }
            catch { /* Ignorer erreurs nettoyage */ }
        }

        private int ComparerVersions(string v1, string v2)
        {
            Version ver1, ver2;
            if (!Version.TryParse(v1, out ver1)) ver1 = new Version(0, 0);
            if (!Version.TryParse(v2, out ver2)) ver2 = new Version(0, 0);
            return ver1.CompareTo(ver2);
        }
    }
}
