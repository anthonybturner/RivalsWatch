from django import template
import ast

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Fetches a dictionary value by key inside Django templates."""
    return dictionary.get(str(key), "")

@register.filter
def to_dict(value):
    """Converts a string representation of a dictionary back into a dictionary."""
    try:
        return ast.literal_eval(value)  # Safely evaluate the string into a Python dictionary
    except (ValueError, SyntaxError):
        return {}  # Return an empty dictionary in case of invalid data