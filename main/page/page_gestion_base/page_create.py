from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QHBoxLayout, QComboBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from main.utils.fonction_diverse.import_modul import importer_module_bdd


class Creation_table_window(QWidget):
    affiche_sql = pyqtSignal(str)

    def __init__(self, module, style_base_donne, connection, choix_bdd):
        super().__init__()
        self.module = module
        self.style_base_donne = style_base_donne
        self.connection = connection
        self.choix_bdd = choix_bdd
        self.module = importer_module_bdd(self.style_base_donne)

        self.setWindowTitle("Création de table")
        self.resize(700, 450)

        layout_principal = QVBoxLayout()
        layout_principal.addWidget(QLabel("Création de table dans la base de données"))

        self.table_name_input = QLineEdit()
        self.table_name_input.setMinimumSize(200, 30)
        self.table_name_input.setMaximumSize(300, 45)
        self.table_name_input.setPlaceholderText("Nom de la table")

        self.combo_type_id = QComboBox()
        self.combo_type_id.addItems([
            "Selectionner la valeur de l'id", "INT", "BIGINT", "SMALLINT",
            "VARCHAR", "TEXT", "DATE", "TIMESTAMP", "SERIAL", "BIGSERIAL"
        ])
        self.combo_type_id.setMinimumSize(200, 30)
        self.combo_type_id.setMaximumSize(300, 45)

        self.combo_contrainte = QComboBox()
        self.combo_contrainte.addItems([
            "Selectionner une contrainte", "Aucune", "NOT NULL", "UNIQUE", "DEFAULT"
        ])
        self.combo_contrainte.setMinimumSize(200, 30)
        self.combo_contrainte.setMaximumSize(300, 45)

        self.default_value_input = QLineEdit()
        self.default_value_input.setPlaceholderText("Valeur par défaut")
        self.default_value_input.setMinimumSize(200, 30)
        self.default_value_input.setMaximumSize(300, 45)
        self.default_value_input.setVisible(False)

        self.combo_clef_primaire = QComboBox()
        self.combo_clef_primaire.addItems([
            "Selectionner un type de clef", "Aucune", "PRIMARY KEY"
        ])
        self.combo_clef_primaire.setMinimumSize(200, 30)
        self.combo_clef_primaire.setMaximumSize(300, 45)

        if self.style_base_donne == "MongoDB":
            self.combo_clef_primaire.setVisible(False)
            self.combo_clef_primaire.setEnabled(False)
            self.default_value_input.setVisible(False)
            self.combo_contrainte.setVisible(False)
            self.combo_type_id.setVisible(False)

        layout_ligne_horizontale = QHBoxLayout()
        layout_ligne_horizontale.addWidget(self.table_name_input)
        layout_ligne_horizontale.addWidget(self.combo_type_id)
        layout_ligne_horizontale.addWidget(self.combo_contrainte)
        layout_ligne_horizontale.addWidget(self.default_value_input)
        layout_ligne_horizontale.addWidget(self.combo_clef_primaire)

        layout_principal.addLayout(layout_ligne_horizontale)

        self.create_button = QPushButton("Créer")
        self.create_button.setMinimumSize(200, 30)
        self.create_button.setMaximumSize(300, 45)
        self.create_button.clicked.connect(self.create_table)
        layout_principal.addWidget(self.create_button)

        self.result_label = QLabel("")
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_principal.addWidget(self.result_label)

        self.setLayout(layout_principal)

        self.combo_type_id.currentTextChanged.connect(self.on_type_id_changed)
        self.combo_contrainte.currentTextChanged.connect(self.on_contrainte_changed)

        self.on_type_id_changed(self.combo_type_id.currentText())

    def on_type_id_changed(self, text):
        if text in ["SERIAL", "BIGSERIAL"]:
            self.combo_contrainte.setCurrentIndex(1)  # "Aucune"
            self.combo_contrainte.setEnabled(False)
            self.default_value_input.setVisible(False)
        else:
            self.combo_contrainte.setEnabled(True)

    def on_contrainte_changed(self, text):
        if text == "DEFAULT":
            self.default_value_input.setVisible(True)
        else:
            self.default_value_input.setVisible(False)
            self.default_value_input.clear()

    def create_table(self):
        connection = self.connection[0] if self.style_base_donne.lower() != "mongodb" else self.connection
        table_name = self.table_name_input.text().strip()
        type_id = self.combo_type_id.currentText()
        contrainte = self.combo_contrainte.currentText()
        clef_primaire = self.combo_clef_primaire.currentText()

        if not table_name:
            self.result_label.setText("Veuillez saisir un nom valide.")
            return

        if self.style_base_donne != "MongoDB":
            if type_id.startswith("Selectionner") or contrainte.startswith("Selectionner") or clef_primaire.startswith("Selectionner"):
                self.result_label.setText("Veuillez sélectionner toutes les options.")
                return

        if self.style_base_donne.lower() == "postgresql":
            if type_id in ("SERIAL", "BIGSERIAL") and contrainte in ("DEFAULT", "NOT NULL"):
                self.result_label.setText(f"Pour {type_id}, la contrainte '{contrainte}' n'est pas nécessaire.")
                return

        elif self.style_base_donne.lower() == "maria":
            if type_id in ("SERIAL", "BIGSERIAL"):
                self.result_label.setText("MariaDB ne supporte pas SERIAL ou BIGSERIAL. Utilisez INT ou BIGINT avec AUTO_INCREMENT.")
                return

        name = self.module.import_query_module("create")

        if self.style_base_donne == "MongoDB":
            try:
                success = name.create(connection, self.choix_bdd, table_name)
                if success:
                    self.result_label.setText(f"Collection '{table_name}' créée avec succès.")
                    self.affiche_sql.emit(f"MongoDB: création collection '{table_name}'")
                else:
                    self.result_label.setText(f"La collection '{table_name}' n'a pas pu être créée (déjà existante ?).")
                    self.affiche_sql.emit(f"MongoDB: échec création collection '{table_name}'")
            except Exception as e:
                self.affiche_sql.emit(f"Erreur MongoDB : {str(e)}")
                self.result_label.setText(f"Erreur lors de la création de la collection : {str(e)}")
        else:
            id_module = self.module.import_query_module("choix_id")
            clef = self.module.import_query_module("clef_primaire")
            obligation = self.module.import_query_module("contrainte")

            clef_style = clef.clef_primaire(clef_primaire)
            valeur_contrainte = obligation.contrainte(contrainte)

            if contrainte == "DEFAULT":
                valeur = self.default_value_input.text().strip()
                if not valeur:
                    self.result_label.setText("Veuillez saisir une valeur pour DEFAULT.")
                    return
                valeur_contrainte = f"DEFAULT '{valeur}'"

            type_colonne = id_module.choix_id(type_id)
            definition_colonne = f"id {type_colonne}"

            if contrainte != "Aucune":
                definition_colonne += f" {valeur_contrainte}"
            if clef_primaire != "Aucune":
                definition_colonne += f" {clef_style}"

            query_name = name.create(table_name)
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
