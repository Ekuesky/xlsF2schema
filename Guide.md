Pour exécuter ce code rapidement dans votre terminal **WSL**, voici les commandes à utiliser selon votre besoin.

### 1. Pour lancer les tests et vérifier les modifications (x-label, bind, etc.)
Depuis la racine de votre projet dans WSL, utilisez cette commande qui définit le `PYTHONPATH` pour inclure le dossier `src` et lance le script de reproduction :

```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
python3 tests/reproduce_issue.py
```

### 2. Pour utiliser l'outil de conversion (CLI)
Si vous voulez convertir un fichier Excel (`.xlsx`) en schéma JSON directement :

```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
python3 src/xlsF2schema/cli.py votre_formulaire.xlsx
```
*Note : Vous pouvez ajouter `-o sortie.json` à la fin pour enregistrer le résultat dans un fichier.*

### 3. Astuce : Rendre la commande permanente (Optionnel)
Pour éviter de taper `export` à chaque fois, vous pouvez installer le projet en mode "éditable" dans votre environnement WSL :

```bash
pip install -e .
```
Une fois cela fait, vous pourrez simplement lancer :
- `xlsF2schema votre_formulaire.xlsx` (partout dans votre terminal)
- `pytest` (pour lancer tous les tests si `pytest` est installé)

### Rappel des prérequis
Assurez-vous d'avoir installé les dépendances nécessaires dans votre instance WSL :
```bash
pip install pyxform
```