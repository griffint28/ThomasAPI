def validate_experience(experience_data):
    if not isinstance(experience_data, list):
        return False

    for entry in experience_data:
        if not isinstance(entry, dict):
            return False

        required_keys = ["title", "company", "years"]
        if not all(key in entry for key in required_keys):
            return False

        if not isinstance(entry["title"], str) or not isinstance(entry["company"], str) or not isinstance(
                entry["years"], str):
            return False
    return True