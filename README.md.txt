pour créer un raccourcis sur le bureau mettre le chemin de python utiliser avec les dépendances puis celle du script qui lance l'application
"C:\Program Files\Python313\python.exe" -m PyInstaller --onefile --add-data "main;main" appli.py

faire le fichier exe en local sur mon ordi perso :
vs code, activé l'environnement, puis python -m PyInstaller --onefile --windowed --add-data "main;main" --add-data ".env;." appli.py

# on separe bien les deux app-data pour les ajouts

En dev → chemins relatifs basés sur __file__ (le fichier .py)

# le chemin en dev n'est pas viable en exe donc prevoir absolument pour évité toute erreur le chemin si dessous dans le path

En exe → chemins basés sur sys.executable (l’emplacement de l’exe)


