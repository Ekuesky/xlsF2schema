import json
from xlsF2schema.core import generate_json_schema

def test_x_label():
    xlsform_data = {
        "children": [
            {
                "type": "text",
                "name": "field_with_string_label",
                "label": "Mon Label String",
            },
            {
                "type": "text",
                "name": "field_with_dict_label",
                "label": {"French": "Mon Label FR", "English": "My EN Label"},

            },
            {
                "type": "text",
                "name": "field_without_label",
            }
        ],
        "choices": {}
    }

    schema = generate_json_schema(xlsform_data)
    items = schema["properties"]["value"]["items"]["properties"]

    # Test field_with_string_label
    print(f"Checking field_with_string_label: {items['field_with_string_label'].get('x-label')}")
    assert items["field_with_string_label"]["x-label"] == "Mon Label String"

    # Test field_with_dict_label
    print(f"Checking field_with_dict_label: {items['field_with_dict_label'].get('x-label')}")
    assert items["field_with_dict_label"]["x-label"] == {"French": "Mon Label FR", "English": "My EN Label"}

    # Test field_without_label
    label_without = items["field_without_label"].get("x-label")
    print(f"Checking field_without_label: {label_without}")
    assert "x-label" not in items["field_without_label"]

def test_bind_attributes():
    xlsform_data = {
        "children": [
            {
                "type": "integer",
                "name": "age",
                "label": "Votre âge",
                "bind": {
                    "relevant": "${consentement} = 'yes'",
                    "constraint": ". > 0 and . < 120",
                    "required": "yes"
                }
            },
            {
                "type": "text",
                "name": "note_interne",
                "bind": {
                    "readonly": "true"
                }
            }
        ],
        "choices": {}
    }
    schema = generate_json_schema(xlsform_data)
    print(json.dumps(schema, indent=4))
    items = schema["properties"]["value"]["items"]["properties"]
    
    assert items["age"]["x-relevant"] == "${consentement} = 'yes'"
    assert items["age"]["x-constraint"] == ". > 0 and . < 120"
    assert items["note_interne"]["x-readOnly"] is True
    print("Bind attributes (relevant, constraint, readonly) checked!")

def test_group_and_repeat_labels():
    xlsform_data = {
        "children": [
            {
                "type": "group",
                "name": "my_group",
                "label": "Group Label",
                "children": [
                    {
                        "type": "text",
                        "name": "subfield",
                        "label": "Sub Label",
                        "bind": {}
                    }
                ]
            },
            {
                "type": "repeat",
                "name": "my_repeat",
                "label": {"fr": "Label Repeat"},
                "children": [
                    {
                        "type": "text",
                        "name": "repfield",
                        "bind": {}
                    }
                ]
            }
        ],
        "choices": {}
    }
    schema = generate_json_schema(xlsform_data)
    print(json.dumps(schema, indent=4))
    items = schema["properties"]["value"]["items"]["properties"]
    
    assert items["my_group"]["x-label"] == "Group Label"
    assert items["my_group"]["properties"]["subfield"]["x-label"] == "Sub Label"
    assert items["my_repeat"]["x-label"] == {"fr": "Label Repeat"}
    assert "x-label" not in items["my_repeat"]["items"]["properties"]["repfield"]
    print("Group and Repeat labels checked!")

if __name__ == "__main__":
    try:
        test_x_label()
        test_bind_attributes()
        test_group_and_repeat_labels()
        print("All tests passed!")
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
