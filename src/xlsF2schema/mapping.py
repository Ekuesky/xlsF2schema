def get_comprehensive_mapping(item, choices_dict):
    """
    Generates a comprehensive mapping dictionary for a given item based on its type and
    optionally retrieves enumeration values from a provided dictionary of choices. This
    function maps XLSForm types to JSON schema types, supporting a wide range of input
    types, including selection, numeric, temporal, geographic, and media types.

    :param item: Dictionary containing details about the item, including its type
     :type item: dict
    :param choices_dict: Dictionary mapping list names to their corresponding enumerations
     :type choices_dict: dict
    :return: A dictionary representing the JSON schema mapping for the given item
     :rtype: dict
    """

    raw_type = item.get('type', 'text').lower().strip()
    xlsform_type = raw_type.split()[0]

    def get_enum(list_name):
        choices = choices_dict.get(list_name, [])
        if choices and isinstance(choices[0], dict):
            return [c.get('name', c.get('label', '')) for c in choices]
        return choices


    # 1. TYPES DE SÉLECTION (CHOICES)
    if xlsform_type in ['select_one', 'select_one_from_file']:
        list_name = raw_type.split()[1] if len(raw_type.split()) > 1 else ''
        return {"type": "string", "enum": get_enum(list_name)}

    if xlsform_type in ['select_multiple', 'select_multiple_from_file']:
        list_name = raw_type.split()[1] if len(raw_type.split()) > 1 else ''
        return {
            "type": "array",
            "items": {"type": "string", "enum": get_enum(list_name)},
            "uniqueItems": True
        }

    if xlsform_type == 'rank':
        list_name = raw_type.split()[1] if len(raw_type.split()) > 1 else ''
        return {
            "type": "array",
            "items": {"type": "string", "enum": get_enum(list_name)},
            "description": "Ranked items in order of preference"
        }

    # 2. TYPES NUMÉRIQUES & TEXTES
    basic_mapping = {
        'integer': {"type": "integer"},
        'decimal': {"type": "number"},
        'text': {"type": "string"},
        'note': {"type": "string", "readOnly": True, "description": "Display-only note"},
        'range': {"type": "number", "description": "Slider/Range component"},
        'acknowledge': {"type": "boolean", "description": "Acknowledgement checkbox"},
        'barcode': {"type": "string", "description": "Scanned barcode data"},
    }

    # 3. TYPES TEMPORELS (Formatage ISO)
    temporal_mapping = {
        'date': {"type": "string", "format": "date"},
        'datetime': {"type": "string", "format": "date-time"},
        'time': {"type": "string", "format": "time"},
        'start': {"type": "string", "format": "date-time", "readOnly": True},
        'end': {"type": "string", "format": "date-time", "readOnly": True},
        'today': {"type": "string", "format": "date", "readOnly": True},
        'deviceid': {"type": "string", "readOnly": True},
        'username': {"type": "string", "readOnly": True},
    }

    # 4. TYPES GÉO (GPS)
    geo_mapping = {
        'geopoint': {
            "type": "object",
            "properties": {
                "latitude": {"type": "number", "minimum": -90, "maximum": 90},
                "longitude": {"type": "number", "minimum": -180, "maximum": 180},
                "altitude": {"type": "number"},
                "accuracy": {"type": "number"}
            },
            "required": ["latitude", "longitude"]
        },
        'geotrace': {
            "type": "object",
            "properties": {
                "type": {"type": "string", "enum": ["LineString"]},
                "coordinates": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {"type": "number"},
                        "minItems": 2
                    }
                },
                "properties": {"type": "object"}
            }
        },
        'geoshape': {
            "type": "object",
            "properties": {
                "type": {"type": "string", "enum": ["Polygon"]},
                "coordinates": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {
                            "type": "array",
                            "items": {"type": "number"},
                            "minItems": 2
                        }
                    }
                },
                "properties": {"type": "object"}
            }
        }
    }

    # 5. TYPES MÉDIAS (FICHIERS)
    media_mapping = {
        'image': {"type": "string", "description": "Image file name/URI"},
        'audio': {"type": "string", "description": "Audio file name/URI"},
        'video': {"type": "string", "description": "Video file name/URI"},
        'file': {"type": "string", "description": "Generic file attachment"},
    }

    # Fusion des dictionnaires par destructuration
    full_mapping = {**basic_mapping, **temporal_mapping, **geo_mapping, **media_mapping}

    return full_mapping.get(xlsform_type, {"type": "string"})