import json

def jsonParser(jsonStr):
    try:
        # Attempt to parse the JSON string
        parsed_data = json.loads(jsonStr)
        return parsed_data
    except json.JSONDecodeError as e:
        # Handle parsing error, such as malformed JSON
        print(f"Failed to parse JSON: {e}")
        return None