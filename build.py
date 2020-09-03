from staticjinja import Site
from datetime import datetime
import json

def dateformat(value, format="%d %b %Y %I:%M %p"):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    if value is None:
        return ""
    return datetime.strptime(value, "%Y-%m-%dT%H:%M").strftime(format)

def streets(street):
    if len(street) == 1:
        return 'on %s' % street[0]
    if len(street) == 2:
        return 'near %s and %s' % (street[0], street[1])
    return ''

def sex2word(value, age):
    if value == 'M':
        if age != '<18':
            return 'man'
        else:
            return 'boy (younger than 18)'
    if value == 'F':
        if age != '<18':
            return 'woman'
        else:
            return 'girl (younger than 18)'
    return value

def ordinal(value):
    """
    Convert an integer to its ordinal as a string. 1 is '1st', 2 is '2nd',
    3 is '3rd', etc. Works for any integer.
    """
    try:
        value = int(value)
    except (TypeError, ValueError):
        return value
    if value % 100 in (11, 12, 13):
        # Translators: Ordinal format for 11 (11th), 12 (12th), and 13 (13th).
        value = '{}th'.format(value)
    else:
        templates = (
            '{}th',
            '{}st',
            '{}nd',
            '{}rd',
            '{}th',
            '{}th',
            '{}th',
            '{}th',
            '{}th',
            '{}th',
        )
        value = templates[value % 10].format(value)
    return value

filters = {
    'dateformat': dateformat,
    'ordinal': ordinal,
    'sex2word': sex2word,
    'streets': streets,
}

if __name__ == "__main__":
    with open("js/shootings_combined.geojson") as f:
        data = json.loads(f.read())

    context = {
        'shootings': [x.get('properties') for x in data.get('features')]
        }
    site = Site.make_site(
        contexts=[('index.html', context)],
        staticpaths=["js/", "css/"],
        filters=filters
        )
    site.render(use_reloader=True)