from StringIO import StringIO
import re

regexp = re.compile(r'([^\\])\$([A-Za-z]+|{.+?})') # oh shi-

def Replacer(template, vars):
    '''Basic replacing template filter.
    Returns a StringIO that looks like a the original file but with
    the keys specified in "vars" replaced like this:
     $abcd => vars['abcd']
     ${anything goes here} => vars['anything goes here']
    '''

    if type(template) != file:
        template = open(template)

    def handle(match):
        blank, key = match.groups()
        key = key.strip("{}")
        if key in vars:
            return blank + str(vars[key])
        else:
            return ''.join(match.groups())

    if not vars:
        return template
    else:
        return StringIO(regexp.sub(handle, template.read()))
