# -*- encoding: utf-8 -*-
from __future__ import with_statement
"""
quote_net is tool for command line tool for display a quote from zitate.net.
"""


__all__ = ['__author__', '__email__','__version__' ,'__license__', 'QuoteRequestException',
           'UnkownResultException','QuoteOptions','extract_quote',
           'retrieve','write_history','out','cl_out']

__author__ = "Alexander Weigl"
__email__  = 'alexweigl <alexweigl@gmail.com>'
__version__= '1.1'
__license__= 'creative commons 3.0 - by-nc-sa <http://creativecommons.org/licenses/by-nc-sa/3.0/de/>'


from datetime import date, time, datetime
from urllib import urlopen, urlencode, quote as urlquote 
from random import randint
from textwrap import wrap
from codecs import open as copen

import xml.etree.ElementTree as ET
import exceptions, sys

from  os.path import expanduser

class QuoteRequestException(exceptions.Exception):
    def __init__(self, message, options = None):
        exceptions.Exception.__init__(self, message)
        self.options = options


class UnkownResultException(exceptions.Exception):
    def __init__(self, message, options = None):
        exceptions.Exception.__init__(self, message)
        self.options = options


class QuoteOptions():
    """
    This class defines the options for the url.
    Sets the options listed below and retrieve with self.tourl() the 
    url for service. You could use retrieve(options) for ElementTree instance.

    
    interval = {0d | 5min | 15min | 1h | 2h | 4h | 12h | 1d | 7d | 30d }

    imagesearchorder = no | author | author, default | 
                       author, subjects, default | subjects |
                       subjects, default | subjects, author, default | default

    entries  = 1..100
    encoding = utf-8
    dateformat = dd.MM.yyyy
    timeformat = HH:mm
    language = de | en | fr ...

    """

    __slots__ = ("interval", "imgsearchorder", "entries", 
                 "encoding", "language", "dateformat", "timeformat")

    BASE_PATH = 'http://zitate.net/xml/zitate..xml'


    def __init__(self, interval="0d", imagesearchorder="default", entries=1, 
                 encoding="utf-8", language="de", 
                 dateformat="dd.MM.yyyy", timeformat="HH:mm"):

        for k,v in iter( locals().items() ) : 
            if k=='self': continue
            self[k] = v      

    def __setattr__(self, key, value):
        self[key]=value
    
    def __getattr__(self, key):
        return self[key]
    

    def __setitem__(self, key, value):
        self.__dict__[key]=value

    def __getitem__(self, key):
        return self.__dict__[key]

    def __str__(self):
        return self.tourl()
        

    def tourl(self):
        return "%s?%s" %( QuoteOptions.BASE_PATH, urlencode(self.__dict__) )
        
def retrieve( options=QuoteOptions() ):    
    """\
    retrieve the xml document from the internet

    if the xml document is a error file it contains no quotes but a error tag. 
    if so this method raise an exception! else it returns the normal xml-document
    """
    handle = urlopen( options.tourl() )
    etree = ET.parse(handle)
    del handle 
    root = etree.getroot() 


    if root.tag == "Quotes":  # Normal case, no error
        return etree
    elif root.tag == 'error': # case of error
        ex = QuoteRequestException( root.text.strip() )
    else:
        ex = UnkownResultExceptio("The xml document is not well-known:\n" + str( etree))
    raise ex

def extract_quote(quote):
    """\
    extracts the necessary information from the xml tag
    returns a dict with text and author
    """
    return {
        'text':    quote.find('Text').text.strip(),
        'author':  quote.find('Author').get('name').strip()
        }
    

def out(text, author):
    """\
    console output for not fancy terminals
    """
    
    print text.encode('utf8')
    print ' ' * 50, '-', author.encode('utf8')

def cl_out(text, author):
    """\
    console output for fancy terminals with colors...
    """
    
    csi = "\033[%sm"
    a = randint(31,36)
    b = randint(31,36)
    c = randint(31,36)
    
    le = 60 
    cnt = le - len(author) - 3

    print csi % a + csi % 1 + "\n".join( wrap( text, le )).encode("utf-8")
    print csi % 0 + csi % b +  ' ' * cnt , '-',
    print csi % c + csi % 4 +  author.encode("utf-8")
    print csi % 0

def write_history(text,author):
    """\
    write the quote to a the history file ~/qhistory in an format that you can use it for fortune (strfile)
    """
    with copen(expanduser('~/.qhistory'), 'a', 'utf8') as fh:
        fh.write(text + "\n")
        fh.write(' ' * 50 + '- ' + author +"\n")
        fh.write("%\n")
