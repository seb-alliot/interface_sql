using Avalonia;
using Avalonia.Controls;
using Avalonia.Markup.Xaml;
using Avalonia.Threading;
using System;
using System.Diagnostics;
using System.IO;
using System.IO.Compression;
using System.Net.Http;
using System.Security.Cryptography;
using System.Text.Json;
using System.Threading.Tasks;
using DotNetEnv;
using Avalonia.Media;

namespace LauncherApp
{
    public partial class LauncherWindow : Window
    {
        private TextBlock labelStatus;
        private Button buttonLancer;
        private string baseDir;
        private string exeActuel;
        private string exeNouveau;

        private Mise_a_jour updateChecker;

        public LauncherWindow()
        {
            InitializeComponent();

            baseDir = AppContext.BaseDirectory;
            exeActuel = Path.Combine(baseDir, "appli_by_itsuki.exe");
            exeNouveau = Path.Combine(baseDir, "appli_by_itsuki_new.exe");

            Env.Load();
            string version = Env.GetString("APP_VERSION");

            Title = $"SQL By Itsuki - v{version}";

            labelStatus = this.FindControl<TextBlock>("StatusLabel")!;
            buttonLancer = this.FindControl<Button>("LancerButton")!;

            buttonLancer.IsEnabled = false;
            buttonLancer.Click += (_, _) => LancerApplication();

            // Initialiser le checker de mise à jour
            updateChecker = new Mise_a_jour(baseDir, exeActuel, exeNouveau);

            updateChecker.OnStatusUpdate += (msg, color) =>
            {
                Dispatcher.UIThread.Post(() =>
                {
                    labelStatus.Text = msg;
                    labelStatus.Foreground = color switch
                    {
                        "red" => new SolidColorBrush(Colors.Red),
                        "green" => new SolidColorBrush(Colors.Green),
                        "cyan" => new SolidColorBrush(Colors.Cyan),
                        "blue" => new SolidColorBrush(Colors.Blue),
                        "yellow" => new SolidColorBrush(Colors.Yellow),
                        _ => new SolidColorBrush(Colors.White),
                    };
                });
            };

            updateChecker.OnUpdateFinished += () =>
            {
                Dispatcher.UIThread.Post(() =>
                {
                    buttonLancer.IsEnabled = true;
                    // Mettre à jour le titre avec la version actuelle dans .env
                    Env.Load();
                    string newVersion = Env.GetString("APP_VERSION");
                    Title = $"SQL By Itsuki - v{newVersion}";
                });
            };

            // Lancer la vérification async
            _ = updateChecker.RunAsync(version);
        }

        private void LancerApplication()
        {
            Env.Load(".env");

            if (File.Exists(exeActuel))
            {
                Process.Start(new ProcessStartInfo(exeActuel, "--from-launcher") { UseShellExecute = true });
                Close();
            }
            else
            {
                labelStatus.Text = "Fichier introuvable : appli_by_itsuki.exe";
                labelStatus.Foreground = new SolidColorBrush(Colors.Red);
            }
        }

        private void InitializeComponent()
        {
            AvaloniaXamlLoader.Load(this);
        }
    }
}
