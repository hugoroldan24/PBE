"""
En el puzzle2 es demana crear una versió gràfica del puzzle1. S'utilitzarà la la biblioteca PyGObject. PyGObject es un binding que permet utilitzar les llibreries basades en GObject com GTK3 que estàn escrites amb C però desde Python.
Per instalar aquesta biblioteca fem: sudo pip3 install PyGObject. Seguidament, descarreguem el paquet gtk3 que es el que conté les funcions per crear la interfaç. sudo apt install libgtk-3-dev. Finalment, instalem el paquet gir1.2-gtk-3.0. Aquest paquet permet a la llibreria PyGObject accedir a les funcionalitats de la llibreria gtk3 desde Python.
sudo apt install gir1.2-gtk-3.0

"""
import gi
import puzzle1 as pz1
gi.require_version("Gtk", "3.0")  #Indiquem que volem fer servir GTK3
from gi.repository import Gtk     #Importem desde el repositori de gi la llibreria Gtk que conté les classes y mètodes per crear la interfaç. 

class Finestra(Gtk.Window):        #Clase relacionada amb la finestra de la aplicació. La classe hereda la clase Gtk.Window de gtk3
    def __init__(self,widgetManager,widgetEditor):
        super().__init__()        #Truquem a la funció __init__ de la classe Gtk.Window
        self.set_title("PUZZLE2") 
        self.set_default_size(400,300)
        self.set_position(Gtk.WindowPosition.CENTER) #Accedeixes a una constant pròpia de Gtk 
        self.widgetManager = widgetManager
        self.widgetEditor = widgetEditor
        
    def configurar_finestra(self):
        text_benvinguda = self.widgetManager.crear_label("""                    Benvingut!
                                          Siusplau, identifique-vos apropant el vostre carnet de la UPC """)
        exit_button = self.widgetManager.crear_boton("Surt")
        
        box_superior = self.widgetManager.crear_box(Gtk.Orientation.HORIZONTAL)           #Creem un botó que col·locarem a la part superior de la finestra
        box_inferior = self.widgetManager.crear_box(Gtk.Orientation.HORIZONTAL)           #Creem un botó que col·locarem a la part inferior de la finestra
        
        self.widgetManager.afegir_widget_box(box_superior,text_benvinguda,True,True,0)    # Introduim el Label de benvinguda al Box superior
        self.widgetManager.afegir_widget_box(box_inferior,exit_button,False,False,0)
        
        self.widgetEditor.configurar_estil(text_benvinguda,"#4682B4","black","0","0")     #Configuramos el estilo del botón Exit en el Box inferior
        self.widgetEditor.configurar_estil(exit_button,"red","black","0","20")            #Configuramos el estilo del Label de bienvenida en el Box superior        

        """Per tal de distribuir les capses de forma que quedi una a sobre de la altre, creo una capsa vertical i considero la capsa inferior i superior com si fossing wadgets. Si configuro que la caixa superior tingui els paràmetrs expand i fill com a True i la inferior com a False, en l'ordre que s'executa el codi quedaràn col·locades com s'espera"""
        box_vertical = self.widgetManager.crear_box(Gtk.Orientation.VERTICAL)
        self.widgetManager.afegir_widget_box(box_vertical,box_superior,False,False,0)    
        self.widgetManager.afegir_widget_box(box_vertical,box_inferior,False,False,0)
        
        self.add(
class widgetManager:
    def __init__(self):
        self.boxes = []
        
    def crear_label(self,text):
        return Gtk.Label(label=text)
        
    def crear_box(self,direccio):
        box = Gtk.Box(orientation=direccio,spacing=1)
        self.boxes.append(box)
        return box
        
    def crear_boton(self,text):
        return Gtk.Button(label=text)
        
    def afegir_widget_box(self,box,widget,expand,fill,padding):
        box.pack_start(widget, expand, fill, padding)
        
class widgetEditor:
    def __init__(self)
        editor_css = Gtk.CssProvider()                                             #Creem l'objecte que controlarà les regles d'estil CSS
        
    def configurar_estil(self,widget,color_fons,color_text,padding,border_radius)
        css = f"""
        *{{
            background-color: {color_fons};  
            color: {color_text};                  
            padding: {padding}px;                  
            border-radius: {border_radius}px;   
        }}
        """
        self.editor_css.load_from_data(css.encode())
        context_estil = widget.get_style_context()
        context_estil.add_provider(self.editor_css,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
                    
if __name__ == "__main__":
      finestra = Finestra(widgetManager(),widgetEditor())
      



