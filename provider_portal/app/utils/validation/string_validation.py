import string


def is_string_valid(s, allowed_characters):
    return all(char in allowed_characters for char in s)


def input_validation(obj, allowed_characters=None):
    if allowed_characters is None:
        allowed_characters = string.ascii_letters + string.digits + string.punctuation + string.whitespace

    if isinstance(obj, str):
        return is_string_valid(obj, allowed_characters)
    elif isinstance(obj, list):
        return all(input_validation(item, allowed_characters) for item in obj)
    elif isinstance(obj, dict):
        return all(input_validation(key, allowed_characters) and input_validation(value, allowed_characters) for key, value in obj.items())
    elif isinstance(obj, tuple):
        return all(input_validation(item, allowed_characters) for item in obj)
    else:
        return False