from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QHBoxLayout, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSignal  # Pour les signaux personnalisés
from main.utils.fonction_diverse.import_modul import importer_module_bdd


class Creation_table_window(QWidget):
    affiche_sql = pyqtSignal(str)
    """
    Fenêtre PyQt6 permettant la création d'une table de base dans une base de données relationnelle.

    Fonctionnalités principales :
    - Saisie du nom de la table à créer.
    - Choix des paramètres pour la colonne "id" (type de données, contrainte, clé primaire).
    - Adaptation automatique de l'interface selon les choix (ex: masquer la valeur par défaut si non pertinente).
    - Gestion spécifique pour PostgreSQL avec vérifications pour éviter les combinaisons invalides.
    - Affichage des erreurs SQL ou succès de la création.

    Limites actuelles :
    - Support uniquement pour PostgreSQL ; MariaDB et MongoDB ne sont pas encore pris en charge.
    - Ne gère que la création d'une table avec une colonne "id". Les autres colonnes doivent être ajoutées dans une autre interface.
    - La valeur par défaut peut être définie uniquement si la contrainte "DEFAULT" est choisie.

    Attributs :
    - module : module dynamique chargé selon le type de base pour générer les requêtes SQL.
    - style_base_donne : type de base de données (ex : "PostgreSQL").
    - connection : connexion active à la base de données.
    - choix_bdd est pas utilisé directement dans cette classe mais
    sert à communiquer ou faire un retour vers une autre fenêtre ou couche de gestion.
    """
    def __init__(self, module, style_base_donne, connection, choix_bdd):
        super().__init__()
        self.module = module
        self.style_base_donne = style_base_donne
        self.connection = connection
        self.choix_bdd = choix_bdd
        self.module = importer_module_bdd(self.style_base_donne)

        self.setWindowTitle("Création de table")
        self.resize(700, 450)

        # === Layout principal vertical ===
        layout_principal = QVBoxLayout()
        layout_principal.addWidget(QLabel("Création de table dans la base de données"))

        # === Ligne horizontale pour le nom de table + paramètres id ===
        self.table_name_input = QLineEdit()
        self.table_name_input.setMinimumSize(200, 30)
        self.table_name_input.setMaximumSize(300, 45)
        self.table_name_input.setPlaceholderText("Nom de la table")

        # === ComboBox pour le type de données (fusionné avec SERIAL) ===
        self.combo_type_id = QComboBox()
        self.combo_type_id.addItems([
            "Selectionner la valeur de l'id", "INT", "BIGINT", "SMALLINT",
            "VARCHAR", "TEXT", "DATE", "TIMESTAMP", "SERIAL", "BIGSERIAL"
        ])
        self.combo_type_id.setMinimumSize(200, 30)
        self.combo_type_id.setMaximumSize(300, 45)

        # === ComboBox pour les contraintes ===
        self.combo_contrainte = QComboBox()
        self.combo_contrainte.addItems([
            "Selectionner une contrainte", "Aucune", "NOT NULL", "UNIQUE", "DEFAULT"
        ])
        self.combo_contrainte.setMinimumSize(200, 30)
        self.combo_contrainte.setMaximumSize(300, 45)

        # === QLineEdit pour valeur DEFAULT (invisible par défaut) ===
        self.default_value_input = QLineEdit()
        self.default_value_input.setPlaceholderText("Valeur par défaut")
        self.default_value_input.setMinimumSize(200, 30)
        self.default_value_input.setMaximumSize(300, 45)
        self.default_value_input.setVisible(False)

        # === Combo pour la clef primaire ===
        self.combo_clef_primaire = QComboBox()
        self.combo_clef_primaire.addItems([
            "Selectionner un type de clef", "Aucune", "PRIMARY KEY"
        ])
        self.combo_clef_primaire.setMinimumSize(200, 30)
        self.combo_clef_primaire.setMaximumSize(300, 45)

        # === Ligne horizontale ===
        layout_ligne_horizontale = QHBoxLayout()
        layout_ligne_horizontale.addWidget(self.table_name_input)
        layout_ligne_horizontale.addWidget(self.combo_type_id)
        layout_ligne_horizontale.addWidget(self.combo_contrainte)
        layout_ligne_horizontale.addWidget(self.default_value_input)
        layout_ligne_horizontale.addWidget(self.combo_clef_primaire)

        layout_principal.addLayout(layout_ligne_horizontale)

        # === Bouton Créer ===
        self.create_button = QPushButton("Créer")
        self.create_button.setMinimumSize(200, 30)
        self.create_button.setMaximumSize(300, 45)
        self.create_button.clicked.connect(self.create_table)
        layout_principal.addWidget(self.create_button)

        # === Résultat ===
        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principal.addWidget(self.result_label)

        # === Appliquer layout ===
        self.setLayout(layout_principal)

        # --- Connexions des signaux ---
        self.combo_type_id.currentTextChanged.connect(self.on_type_id_changed)
        self.combo_contrainte.currentTextChanged.connect(self.on_contrainte_changed)

        # Initialisation du filtre
        self.on_type_id_changed(self.combo_type_id.currentText())

    def on_type_id_changed(self, text):
        """
        Gère les changements dans le choix du type de la colonne 'id'.

        - Si le type est SERIAL ou BIGSERIAL (types auto-incrémentés de PostgreSQL),
        désactive la sélection de contrainte et masque le champ valeur par défaut,
        car ces contraintes ne sont pas nécessaires ni compatibles.
        - Sinon, réactive la sélection de contrainte.
        """
        # Si SERIAL ou BIGSERIAL, désactiver la contrainte par défaut
        if text in ["SERIAL", "BIGSERIAL"]:
            self.combo_contrainte.setCurrentIndex(1)  # "Aucune"
            self.combo_contrainte.setEnabled(False)
            self.default_value_input.setVisible(False)
        else:
            self.combo_contrainte.setEnabled(True)

    def on_contrainte_changed(self, text):
        """
        Gère les changements dans le choix de contrainte pour la colonne 'id'.

        - Si la contrainte sélectionnée est 'DEFAULT', affiche le champ pour saisir
        la valeur par défaut.
        - Sinon, masque ce champ et le vide.
        """
        # Affiche ou masque le champ pour la valeur par défaut
        if text == "DEFAULT":
            self.default_value_input.setVisible(True)
        else:
            self.default_value_input.setVisible(False)
            self.default_value_input.clear()

    def create_table(self):
        """
        Récupère les paramètres saisis, valide les choix et construit la requête SQL
        pour créer une table avec une colonne 'id' en fonction des options sélectionnées.

        - Vérifie que le nom de table et les options sont valides.
        - Applique des règles spécifiques à PostgreSQL (ex: SERIAL ne doit pas avoir DEFAULT ou NOT NULL explicite).
        - Utilise des modules dynamiques pour générer les fragments de la requête SQL.
        - Exécute la requête SQL via la connexion.
        - Affiche un message de succès ou d'erreur selon le résultat.

        Note : la colonne créée est uniquement "id" avec les paramètres choisis.
        """
        connection = self.connection[0]

        table_name = self.table_name_input.text().strip()
        type_id = self.combo_type_id.currentText()
        contrainte = self.combo_contrainte.currentText()
        clef_primaire = self.combo_clef_primaire.currentText()

        if not table_name:
            self.result_label.setText("Veuillez saisir un nom valide.")
            return

        if type_id.startswith("Selectionner") or contrainte.startswith("Selectionner") or clef_primaire.startswith("Selectionner"):
            self.result_label.setText("Veuillez sélectionner toutes les options.")
            return

        # Vérification style base de donnée
        if self.style_base_donne.lower() == "PostgreSQL":
            # Restrictions et adaptations pour Postgres
            # Ex : SERIAL ne doit pas avoir DEFAULT ni NOT NULL explicitement
            if type_id in ("SERIAL", "BIGSERIAL"):
                if contrainte in ("DEFAULT", "NOT NULL"):
                    self.result_label.setText(f"Pour {type_id}, la contrainte '{contrainte}' n'est pas nécessaire.")
                    return
            # autres règles Postgres ici si besoin

        elif self.style_base_donne.lower() == "maria":
            self.result_label.setText("MariaDB non supporté pour le moment.")
            return

        elif self.style_base_donne.lower() == "mongo":
            self.result_label.setText("MongoDB non supporté pour le moment.")
            return

        # Import des modules
        name = self.module.import_query_module("create")
        id_module = self.module.import_query_module("choix_id")
        clef = self.module.import_query_module("clef_primaire")
        obligation = self.module.import_query_module("contrainte")

        query_name = name.create(table_name)
        clef_style = clef.clef_primaire(clef_primaire)
        valeur_contrainte = obligation.contrainte(contrainte)

        type_colonne = id_module.choix_id(type_id)
        definition_colonne = f"id {type_colonne}"

        if contrainte != "Aucune":
            definition_colonne += f" {valeur_contrainte}"
        if clef_primaire != "Aucune":
            definition_colonne += f" {clef_style}"

        requete = query_name(definition_colonne)
        self.affiche_sql.emit(requete)


        cursor = connection.cursor()
        try:
            cursor.execute(requete)
            connection.commit()
            self.result_label.setText(f"Table '{table_name}' créée avec succès.")
        except Exception as e:
            connection.rollback()
            self.affiche_sql.emit(f"Erreur SQL : {str(e)}\nRequête : {requete}")
            self.result_label.setText(f"Erreur lors de la création de la table : {str(e)}")
