"""
Tests unitaires pour la conversion XLSForm vers JSON Schema
"""
import pytest
import json
from pathlib import Path
from xlsF2schema.core import generate_json_schema

# Chemin vers les fichiers de test
SAMPLES_DIR = Path(__file__).parent / "samples"


def test_generate_json_schema_basic():
    """Test de conversion basique avec des champs simples"""
    xlsform_data = {
        "children": [
            {
                "type": "text",
                "name": "nom",
                "bind": {"required": "yes"}
            },
            {
                "type": "integer",
                "name": "age",
                "bind": {"required": "no"}
            }
        ],
        "choices": {}
    }

    schema = generate_json_schema(xlsform_data)

    assert schema["$schema"] == "http://json-schema.org/draft-07/schema#"
    assert schema["type"] == "object"
    assert "value" in schema["properties"]
    assert schema["properties"]["value"]["type"] == "array"

    items = schema["properties"]["value"]["items"]
    assert "nom" in items["properties"]
    assert "age" in items["properties"]
    assert "nom" in items["required"]
    assert "age" not in items["required"]


def test_generate_json_schema_with_group():
    """Test de conversion avec des groupes"""
    xlsform_data = {
        "children": [
            {
                "type": "group",
                "name": "info_personnelle",
                "children": [
                    {
                        "type": "text",
                        "name": "prenom",
                        "bind": {"required": "yes"}
                    },
                    {
                        "type": "text",
                        "name": "nom",
                        "bind": {"required": "yes"}
                    }
                ]
            }
        ],
        "choices": {}
    }

    schema = generate_json_schema(xlsform_data)
    items = schema["properties"]["value"]["items"]

    assert "info_personnelle" in items["properties"]
    assert items["properties"]["info_personnelle"]["type"] == "object"
    assert "prenom" in items["properties"]["info_personnelle"]["properties"]
    assert "nom" in items["properties"]["info_personnelle"]["properties"]


def test_generate_json_schema_with_repeat():
    """Test de conversion avec des sections répétables"""
    xlsform_data = {
        "children": [
            {
                "type": "repeat",
                "name": "membres_famille",
                "children": [
                    {
                        "type": "text",
                        "name": "nom_membre",
                        "bind": {"required": "yes"}
                    },
                    {
                        "type": "integer",
                        "name": "age_membre",
                        "bind": {}
                    }
                ]
            }
        ],
        "choices": {}
    }

    schema = generate_json_schema(xlsform_data)
    items = schema["properties"]["value"]["items"]

    assert "membres_famille" in items["properties"]
    assert items["properties"]["membres_famille"]["type"] == "array"
    assert "items" in items["properties"]["membres_famille"]

    repeat_items = items["properties"]["membres_famille"]["items"]
    assert repeat_items["type"] == "object"
    assert "nom_membre" in repeat_items["properties"]
    assert "age_membre" in repeat_items["properties"]


def test_generate_json_schema_nullable_fields():
    """Test que les champs non requis acceptent null"""
    xlsform_data = {
        "children": [
            {
                "type": "text",
                "name": "champ_optionnel",
                "bind": {}
            }
        ],
        "choices": {}
    }

    schema = generate_json_schema(xlsform_data)
    items = schema["properties"]["value"]["items"]

    field_type = items["properties"]["champ_optionnel"]["type"]
    assert isinstance(field_type, list)
    assert "null" in field_type


def test_generate_json_schema_empty():
    """Test avec un XLSForm vide"""
    xlsform_data = {
        "children": [],
        "choices": {}
    }

    schema = generate_json_schema(xlsform_data)

    assert schema["$schema"] == "http://json-schema.org/draft-07/schema#"
    assert schema["type"] == "object"
    items = schema["properties"]["value"]["items"]
    assert items["properties"] == {}


def test_generate_json_schema_no_required():
    """Test que la clé 'required' est absente si aucun champ n'est requis"""
    xlsform_data = {
        "children": [
            {
                "type": "text",
                "name": "optionnel",
                "bind": {}
            }
        ],
        "choices": {}
    }

    schema = generate_json_schema(xlsform_data)
    items = schema["properties"]["value"]["items"]

    assert "required" not in items


def test_generate_json_schema_with_choices():
    """Test avec des choix (select_one/select_multiple)"""
    xlsform_data = {
        "children": [
            {
                "type": "select one",
                "name": "genre",
                "itemset": "genres",
                "bind": {"required": "yes"}
            }
        ],
        "choices": {
            "genres": [
                {"name": "homme", "label": "Homme"},
                {"name": "femme", "label": "Femme"}
            ]
        }
    }

    schema = generate_json_schema(xlsform_data)
    items = schema["properties"]["value"]["items"]

    assert "genre" in items["properties"]
    assert "genre" in items["required"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
