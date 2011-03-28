
import config

import re
import subprocess

def mail(to="", subject="", text="", html=True, **headers):
    '''All arguments may be called as keyword arguments.
    Unknown arguments are interpreted as extra headers.
    This is useful to add the From field:
        mail(..., From="webmaster@example.com")
    Underscores are replaced with dashes in headers:
        mail(..., Content_Type="text/html")
    Newlines are stripped from header values.
    From and To fields are validated. Returns False on any error.
    '''
    
    headers.setdefault('Subject', subject)
    headers.setdefault('From', config.DEFAULT_FROM)
    headers['To'] = to
    
    if not is_valid_email(to) or not is_valid_email(headers['From']):
        return False
    
    if html:
        headers.setdefault('Content_Type', "text/html")

    try:
        process = subprocess.Popen([config.SENDMAIL_PATH, '-t', to],
            stdin=subprocess.PIPE)
    except OSError:
        return False

    for key, value in headers.iteritems():
        process.stdin.write("%s: %s\n" % (key.replace("_", "-"),
                                          value.replace("\n", "")))
    process.stdin.write("\n")
    process.stdin.write(text)
    process.stdin.flush()
    process.stdin.close()
    return process.wait() == 0

valid_re = re.compile('^([a-z0-9\+_\-]+)(\.[a-z0-9\+_\-]+)*@([a-z0-9\-]+\.)+[a-z]{2,6}$', re.I)
valid2_re = re.compile('^[\w \.\'"-]* <(.*)>$', re.UNICODE)
def is_valid_email(email):
    '''Regexp stolen from "somewhere"'''
    email = email.decode("utf-8", "replace")
    if valid_re.match(email) is not None:
        return True
    else:
        matchobj = valid2_re.match(email)
        if matchobj is not None:
            return valid_re.match(matchobj.group(1)) is not None
    return False

