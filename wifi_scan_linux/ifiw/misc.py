import re
import locale
import string

def Regex(regex, s):
    """ runs a regex search on a string 
        regex -- The pattern that should be matched
        s     -- the string that should be searched
    """
    m = regex.search(s)
    if m:
        return m.groups()[0]
    else:
        return None
def sanitize_escaped(s):
    """ Sanitize double-escaped unicode strings. """
    lastpos = -1
    while True:
        lastpos = s.find('\\x', lastpos + 1)
        #print lastpos
        if lastpos == -1:
            break
        c = s[lastpos+2:lastpos+4]  # i.e. get the next two characters
        s = s.replace('\\x'+c, chr(int(c, 16)))
    return s

def to_unicode(x):
    """ Attempts to convert a string to utf-8. """
    # If this is a unicode string, encode it and return
    if not isinstance(x, str):
        return x

    x = sanitize_escaped(x)

    ret = x
#    try:
#        ret = x.encode('utf-8')
#    except UnicodeError:
#        try:
#            ret = x.decode('latin-1').encode('utf-8')
#        except UnicodeError:
#            ret = x.decode('utf-8', 'replace').encode('utf-8')
            
    return ret
