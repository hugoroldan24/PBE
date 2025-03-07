"""
En el puzzle2 es demana crear una versió gràfica del puzzle1. S'utilitzarà la la biblioteca PyGObject. PyGObject es un binding que permet utilitzar les llibreries basades en GObject com GTK3 que estàn escrites amb C però desde Python.
Per instalar aquesta biblioteca fem: sudo pip3 install PyGObject. Seguidament, descarreguem el paquet gtk3 que es el que conté les funcions per crear la interfaç. sudo apt install libgtk-3-dev. Finalment, instalem el paquet gir1.2-gtk-3.0. Aquest paquet permet a la llibreria PyGObject accedir a les funcionalitats de la llibreria gtk3 desde Python.
sudo apt install gir1.2-gtk-3.0

"""
import gi
import puzzle1 as pz1
from gi.repository import Gtk  

if __name__ == "__main__":
  



