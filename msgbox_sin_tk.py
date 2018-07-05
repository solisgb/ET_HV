#!/usr/bin/env python
# coding: latin-1
        
def ask_overwrite(path, window_title='Confirm overwrite' ):
    """
    pregunta si sobreescribe y devuelve True o False
    """
    from os.path import isfile
    from tkinter import messagebox as mBox
    from tkinter import Tk
    if isfile(path):
        root=Tk()
        root.withdraw()
        a=mBox.askyesno(window_title, 'el fichero\n{}\nya existe\nSOBREESCRIBIR?'.format(path))
        return a
    return True

def ask_continue(msg, window_title='Confirm continue' ):
    """
    pregunta si continua a la luz del contenido de msg y devuelve True o False
    """
    from tkinter import messagebox as mBox
    from tkinter import Tk
    root=Tk()
    root.withdraw()
    a=mBox.askyesno(window_title, msg)
    return a

def proceso_terminado(msg, window_title='Aviso de proceso terminado' ):
    """
    aviso de proceso terminado
    """
    from tkinter import messagebox as mBox
    from tkinter import Tk
    root=Tk()
    root.withdraw()
    mBox.showinfo(window_title, msg)

def mostrar_error(msg, window_title='Se ha producido un error'):
    """
    aviso de error
    """
    from tkinter import messagebox as mBox
    from tkinter import Tk
    root=Tk()
    root.withdraw()
    a=mBox.showerror(window_title, msg)
    print(a)
