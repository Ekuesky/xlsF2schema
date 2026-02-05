from .mapping import get_comprehensive_mapping


def generate_json_schema(xlsform_dict_data:dict):
    """
    Génère un JSON Schema à partir d'un dictionnaire XLSForm (pyxform).
    """
    survey_tab = xlsform_dict_data.get("children", [])
    choices_tab = xlsform_dict_data.get("choices", {})

    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "value": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }
    }
    
    target_properties = schema["properties"]["value"]["items"]["properties"]
    target_required = schema["properties"]["value"]["items"]["required"]

    def process_items(items, properties_dict, required_list):
        """
        Traite une liste d'éléments et les structure dans un format de dictionnaire imbriqué
        représentant leur schéma, y compris leur type, leurs propriétés, leurs champs obligatoires
        et d'autres attributs. Gère différents types d'éléments tels que les groupes et les champs répétables
        , en traitant de manière récursive les enfants s'ils sont présents.

        :param items:
            La liste des éléments à traiter. Chaque élément de la liste doit être un dictionnaire
            avec des clés telles que « type », « nom » et « enfants » (facultatif).
        :type items: list[dict]

        :param properties_dict:
            Un dictionnaire qui sera rempli avec le schéma des éléments fournis.
            Les clés sont les noms d'éléments et les valeurs sont leur schéma correspondant.
        :type properties_dict: dict

        :param required_list:
            Une liste qui sera remplie avec les noms des éléments marqués comme
            requis.
        :type required_list: list

        :return:
            Cette fonction ne renvoie pas de valeur. Il modifie `properties_dict` et
            `required_list` en place.
        :rtype: None
        """

        for item in items:
            item_type = item.get("type", "")
            name = item.get("name")
            if not name:
                continue

            if item_type == "group":
                sub_props = {}
                sub_required = []
                properties_dict[name] = {
                    "type": "object",
                    "properties": sub_props,
                    "required": sub_required
                }
                if "children" in item:
                    process_items(item["children"], sub_props, sub_required)
                if not sub_required:
                    properties_dict[name].pop("required")

            elif item_type == "repeat":
                sub_props = {}
                sub_required = []
                properties_dict[name] = {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": sub_props,
                        "required": sub_required
                    }
                }
                if "children" in item:
                    process_items(item["children"], sub_props, sub_required)
                if not sub_required:
                    properties_dict[name]["items"].pop("required")

            else:
                # Field mapping
                field_schema = get_comprehensive_mapping(item, choices_tab)
                is_required = str(item.get("bind", {}).get("required")).lower() in ["yes", "true"]
                #TODO à ajouter
                has_relevant = item.get("bind", {}).get("relevant") is not None


                # Autoriser null pour que les champs non obligatoires correspondent aux ensembles de données en utilisant des valeurs nulles explicites
                if not is_required:
                    t = field_schema.get("type")
                    if isinstance(t, str):
                        field_schema["type"] = [t, "null"]
                    elif isinstance(t, list):
                        if "null" not in t:
                            field_schema["type"] = t + ["null"]
                    else:
                        # If no type specified, default to allowing null
                        field_schema["type"] = ["string", "null"]

                properties_dict[name] = field_schema

                if is_required:
                    required_list.append(name)

    process_items(survey_tab, target_properties, target_required)

    # Si target_required est vide alors on soustrait la clé required du schema (ce n'est pas obligatoire)
    if not target_required:
        schema["properties"]["value"]["items"].pop("required")
        
    return schema
