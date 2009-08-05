
import config

import subprocess

def mail(to="", subject="", text="", html=True, **headers):
    '''All arguments may be called as keyword arguments.
    Unknown arguments are interpreted as extra headers.
    This is useful to add the From field:
        mail(..., From="webmaster@example.com")
    Underscores are replaced with dashes in headers:
        mail(..., Content_Type="text/html")
    Newlines are stripped from header values.
    '''
    process = subprocess.Popen([config.SENDMAIL_PATH, '-t', to],
        stdin=subprocess.PIPE)

    if 'Subject' not in headers:
        headers['Subject'] = subject

    if 'From' not in headers and config.DEFAULT_FROM:
        headers['From'] = config.DEFAULT_FROM

    if html and 'Content_Type' not in headers:
        headers['Content_Type'] = "text/html"

    for key, value in headers.iteritems():
        process.stdin.write("%s: %s\n" % (key.replace("_", "-"),
                                          value.replace("\n", "")))
    process.stdin.write("\n")
    process.stdin.write(text)
