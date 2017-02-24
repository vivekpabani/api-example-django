from django import template

register = template.Library()

@register.simple_tag
def get_greeting_message(fname, lname, duration, doc_name="Your Doctor"):

    templates = ['I guess I missed your birthday. ',
                 'It is your birthday today! ',
                 'Your birthday is coming soon! ']

    idx, belated, advanced = 0, '', ''

    if duration < 0:
        idx = 0
        belated = " belated"
    elif duration == 0:
        idx = 1
    else:
        idx = 2
        advanced = " in advance"

    message = 'Hey {} {},\\n\\n{}Wish you a{} happy birthday{}!\\n\\nRegards,\\n{}'.format(fname,
                                                                            lname,
                                                                            templates[idx],
                                                                            belated, advanced, doc_name)
    return message
