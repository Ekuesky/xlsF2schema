import json
import argparse
import sys
from pyxform.builder import create_survey_from_path
from xlsF2schema.core import generate_json_schema

def xlsform_to_dict(path):
    """
    Transforme un fichier XLSForm en dictionnaire via pyxform.
    """
    survey = create_survey_from_path(path)
    return survey.to_json_dict()

def main():
    parser = argparse.ArgumentParser(description="Convertir un XLSForm en JSON Schema via pyxform")
    parser.add_argument("input", help="Chemin vers le fichier XLSForm (.xlsx ou .xls)")
    parser.add_argument("-o", "--output", help="Chemin du fichier JSON Schema de sortie (défaut: affiche sur stdout)")
    
    args = parser.parse_args()
    
    try:
        # 1. Charger le fichier et transformer en dict
        xlsform_dict = xlsform_to_dict(args.input)
        
        # 2. Dégager le schéma
        schema = generate_json_schema(xlsform_dict)
        
        # 3. Sortie
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(schema, f, indent=4, ensure_ascii=False)
            print(f"Schéma généré avec succès dans : {args.output}")
        else:
            print(json.dumps(schema, indent=4, ensure_ascii=False))
            
    except Exception as e:
        print(f"Erreur : {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
