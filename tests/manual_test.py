import json
from src.xlsF2schema.core import generate_json_schema

# Mock survey_dict basé sur l'exemple JSON fourni et la structure XLSForm
survey_dict = {
    "children": [
        {"type": "date", "name": "date", "label": "Date"},
        {"type": "start", "name": "start", "label": "Start"},
        {
            "type": "group",
            "name": "gr_enqueter",
            "label": "Groupe Enquêteur",
            "children": [
                {"type": "select_one list_enqueteurs", "name": "enqueteur", "label": "Enquêteur"},
                {"type": "text", "name": "enqueteur_autre", "label": "Autre"},
                {"type": "select_one list_sous_cat", "name": "sous_cat", "label": "Sous-catégorie"},
                {"type": "text", "name": "sous_cat_autre", "label": "Autre"},
                {"type": "text", "name": "cible_point_gps", "label": "Cible"},
                {"type": "geopoint", "name": "point_gps", "label": "Point GPS"},
                {"type": "geotrace", "name": "trace_gps", "label": "Trace GPS"},
                {"type": "text", "name": "sujet_photo", "label": "Sujet photo"},
                {"type": "image", "name": "photo", "label": "Photo"}
            ]
        },
        {
            "type": "group",
            "name": "meta",
            "children": [
                {"type": "text", "name": "instanceID", "bind": {"required": "yes"}}
            ]
        }
    ],
    "choices": {
        "list_enqueteurs": [{"name": "enqueteurA", "label": "A"}, {"name": "enqueteurB", "label": "B"}],
        "list_sous_cat": [{"name": "releve_trace_gps", "label": "Relevé trace GPS"}]
    }
}

schema = generate_json_schema(survey_dict)
print(json.dumps(schema, indent=2))

# Test data validation
test_data = {
	"value": [
		{
			"date": "2026-02-02",
			"start": "2026-02-02T15:50:21.966-00:00",
			"gr_enqueter": {
				"enqueteur": "enqueteurA",
				"enqueteur_autre": None,
				"sous_cat": "releve_trace_gps",
				"sous_cat_autre": None,
				"cible_point_gps": None,
				"point_gps": None,
				"trace_gps": {
					"type": "LineString",
					"coordinates": [
						[-67.243881, 54.953864, 0],
						[-67.290571, 55.039041, 0],
						[-67.378146, 55.005952, 0],
						[-67.24384, 54.953569, 1]
					],
					"properties": {
						"accuracies": [None, None, None, 0.4]
					}
				},
				"sujet_photo": None,
				"photo": None
			},
			"meta": {
				"instanceID": "uuid:a2df652c-6bc1-46e0-b388-780f93e85cfc"
			}
		}
	]
}

try:
    from jsonschema import validate
    validate(instance=test_data, schema=schema)
    print("Validation SUCCESSFUL!")
except ImportError:
    print("jsonschema not installed, skipping validation check.")
except Exception as e:
    print(f"Validation FAILED: {e}")
