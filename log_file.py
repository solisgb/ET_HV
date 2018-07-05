#!/usr/bin/env python
# coding: latin-1

import io

class Log_file(object):
    """
    descripción
    """
    _contents=io.StringIO()
    _dst='log.txt'

    @staticmethod
    def contents_get():
        from time import gmtime, strftime
        a=Log_file._contents.getvalue()
        if len(a)==0:
            return strftime("%a, %d %b %Y %H:%M:%S +0000\n", gmtime())
        else:
            return Log_file._contents.getvalue()

    @staticmethod
    def write(str1=None, lista_str=[]):
        if str1!=None:
            Log_file._contents.write('{}\n'.format(str1))
        
        if len(lista_str)>0:
            for str1 in lista_str:
                Log_file._contents.write('{}\n'.format(str1))

    @staticmethod
    def toFile():
        """
        descripción
        """
        from time import gmtime, strftime
        try:
            
            d=strftime("%a, %d %b %Y %H:%M:%S +0000\n", gmtime())
            a=Log_file._contents.getvalue()
            
            f=open(Log_file._dst, 'w')
            f.write('{}'.format(d))
            f.write('{}'.format(a))
            f.close()
            
        except:
            pass
        
