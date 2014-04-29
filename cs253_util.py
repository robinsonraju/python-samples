import cgi

def escape_html(s):
    ''' (str) -> str
    Escape HTML tags input string s

    >>> escape_html('<input>')
    '&lt;input&gt;'
    
    '''
    return cgi.escape(s, quote = True)
