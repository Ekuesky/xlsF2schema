# xlsF2schema 📊 ➡️ 📜

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)

**xlsF2schema** est un convertisseur robuste et flexible permettant de transformer vos fichiers **XLSForm** (utilisés par ODK, KoBoToolbox, etc.) en schémas **JSON Schema** (Draft 07).

Il facilite l'intégration de vos formulaires de collecte de données dans des systèmes web modernes, permettant la validation de données coté serveur ou la génération automatique d'interfaces utilisateur.

---

## ✨ Fonctionnalités

- **Conversion Complète** : Supporte la majorité des types de champs ODK/XLSForm.
- **Structure Hiérarchique** : Gère parfaitement les `groups` et les `repeats` de manière récursive.
- **Validation Intégrée** : 
  - Extraction des contraintes `required`.
  - Support des listes de choix (`select_one`, `select_multiple`) via les `enums` JSON Schema.
  - Gestion des types complexes : `geopoint`, `geotrace`, `geoshape`.
- **Flexibilité** : Autorise les valeurs `null` pour les champs non obligatoires.
- **Interface Double** : Utilisation simple via la ligne de commande (CLI) ou intégration directe en tant que bibliothèque Python.

---

## 🚀 Installation

Vous pouvez installer **xlsF2schema** via `pip` :

```bash
pip install xlsF2schema
```

---

## 🛠️ Utilisation via CLI

La commande `xlsF2schema` est disponible immédiatement après l'installation.

### Générer un schéma et l'afficher
```bash
xlsF2schema mon_formulaire.xlsx
```

### Enregistrer le schéma dans un fichier
```bash
xlsF2schema mon_formulaire.xlsx -o schema.json
```

---

## 🐍 Utilisation en Python

Vous pouvez également intégrer le convertisseur dans vos propres scripts Python :

```python
from xlsF2schema.cli import xlsform_to_dict
from xlsF2schema.core import generate_json_schema

# 1. Charger le XLSForm en dictionnaire (via pyxform)
xlsform_data = xlsform_to_dict("chemin/vers/formulaire.xlsx")

# 2. Générer le JSON Schema
schema = generate_json_schema(xlsform_data)

# Utiliser le schéma (ex: validation avec jsonschema)
import json
print(json.dumps(schema, indent=4))
```

---

## 📋 Format du Schéma Généré

Le schéma produit par **xlsF2schema** utilise une structure enveloppante (`wrapper`) conçue pour valider des collections d'enregistrements (typiquement des exports de données) :

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "value": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "champ_1": { "type": "string" },
          "champ_2": { "type": "integer" }
        }
      }
    }
  }
}
```

Cela permet de valider directement les fichiers JSON contenant plusieurs soumissions.

---

## 🗺️ Mappage des Types (Aperçu)

| Type XLSForm | Type JSON Schema | Détails |
| :--- | :--- | :--- |
| `text`, `integer`, `decimal` | `string`, `integer`, `number` | Correspondance directe. |
| `select_one` | `string` | Utilise `enum` avec les noms des choix. |
| `select_multiple` | `array` | `uniqueItems: true`. |
| `date`, `datetime`, `time` | `string` | Format `date`, `date-time`, `time`. |
| `geopoint` | `object` | Propriétés `latitude`, `longitude`, `altitude`, `accuracy`. |
| `group` | `object` | Propriétés imbriquées. |
| `repeat` | `array` | Tableau d'objets. |

---

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Forker le projet.
2. Créer une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`).
3. Commiter vos changements (`git commit -m 'Add some AmazingFeature'`).
4. Pusher vers la branche (`git push origin feature/AmazingFeature`).
5. Ouvrir une Pull Request.

---

## 📄 Licence

Distribué sous la licence MIT. Voir `LICENSE` pour plus d'informations.

---

**Développé avec ❤️ par [AYIEK SKY](mailto:ayiekue@outlook.com)**