xlsF2schema/
├── pyproject.toml           # Configuration moderne du build (remplace setup.py)
├── README.md                # Documentation pour les utilisateurs
├── LICENSE                  # Licence logicielle (MIT, Apache, etc.)
├── src/                     # Code source (pattern "src-layout" recommandé)
│   └── xlsF2schema/
│       ├── __init__.py      # Rend le dossier importable
│       ├── core.py          # Logique principale de conversion
│       ├── mapping.py       # Dictionnaire exhaustif des types ODK
│       ├── utils.py         # Fonctions utilitaires (nettoyage CSV, regex)
│       └── cli.py           # Interface en ligne de commande
├── tests/                   # Tests unitaires
│   ├── __init__.py
│   ├── test_conversion.py
│   └── samples/             # Fichiers XLSForm de test
└── examples/                # Exemples d'utilisation