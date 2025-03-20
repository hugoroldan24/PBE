"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
En el puzzle2 es demana crear una versió gràfica del puzzle1. S'utilitzarà la la biblioteca PyGObject. PyGObject es un binding que permet utilitzar les llibreries basades en GObject com GTK3 que estàn escrites amb C però desde Python.
Per instalar aquesta biblioteca fem: sudo pip3 install PyGObject. Seguidament, descarreguem el paquet gtk3 que es el que conté les funcions per crear la interfaç. sudo apt install python3-gi (bindings de GTK para python. Finalment, instalem el paquet gir1.2-gtk-3.0. Aquest paquet permet a la llibreria PyGObject accedir a les funcionalitats de la llibreria gtk3 desde Python.
sudo apt install gir1.2-gtk-3.0
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import gi
import puzzle1 
import threading 
gi.require_version("Gtk", "3.0")                                       #Indiquem que volem fer servir GTK3
from puzzle1Llibreria.puzzle1 import Rfid_522
from gi.repository import Gtk, GLib, Gdk                               #Importem desde el repositori de gi la llibreria Gtk i GLib i que contenen les classes i mètodes per crear la interfaç i interactuar amb threads auxiliars respectivamente. 

WELCOME_STRING = "Please, login with your university card"


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Classe per configurar la finestra d'una aplicació i els seus elements. La classe hereda els mètodes de la classe Gtk.ApplicationWindow
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class MyWindow(Gtk.ApplicationWindow):  
    """
    Inicialitza un objecte de la classe Gtk.ApplicationWindow i de la classe Rfid_522() del puzzle1.
    """   
    def __init__(self):
        super().__init__()                                                 #Cridem a la funció __init__ de la classe Gtk.ApplicationWindow.
        self.myReader = puzzle1.Rfid_522()                                 #Instancia un objecte de la classe Rfid_522() del puzzle1.
        self.editor_css = Gtk.CssProvider()
      
    """ 
    Configura la finestra amb els paràmetres escollits.
    Paràmetres:
        :amplada:    Amplada de la finestra
        :altura:     Altura de la finestra
        :posició: Posició de la finestra a la pantalla
        :titol: Títol de la finestra
    """
    def configure_window(self,amplada,altura,posició,titol):
        self.set_title(titol) 
        self.set_default_size(amplada,altura)
        self.set_position(posició)                                                                              #Posició de la finestra a la pantalla
      
    """
    Instancia totes les capses que es faràn servir, les configura i les afegeix a la finestra.
    """
    def start_boxes(self):            
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=0)                                  #Creem una capsa amb orientació vertical
        self.add(self.main_box)                                                                                  #Afegim la capsa a la finestra
             
    """
    Instancia els labels que es faràn servir inicialment i els introdueix a la capsa principal
    """
    def start_labels(self):
        self.welcome_label = Gtk.Label(label=WELCOME_STRING)                                                  #Creem el label amb el text passat per paràmetre
        self.main_box.pack_start(self.welcome_label, False, False, 0)                                        #Afegim el label al inici de la capsa vertical (part superior)
        self.welcome_label.set_name("welcome_label")                                                         #Assignem una ID al label
        
    """
    Instancia els botons que es faràn servil inicialmente. Configura les seves característiques i els afegeix a la capsa
    """
    def start_buttons(self):
        self.exit_button = Gtk.Button(label="Exit")                                                          #Creem el botó Exit.
        self.exit_button.connect("clicked",Gtk.main_quit)                                                    #Terminem la finestra quan pressionem el botó.
        self.main_box.pack_end(self.exit_button, False, False, 0)                                            #Afegim el botó al final de la capsa vertical (part inferior)
        self.exit_button.set_name("exit_button")                                                             #Assignem una ID al botó
        
        self.clear_button = Gtk.Button(label="Clear")                                                        #Creem el botó Clear
        self.clear_button.connect("clicked",self.reset_window)                                               #S'executarà el mètode reset_window() quan es pressioni el botó "Clear"
        self.main_box.pack_end(self.clear_button, False, False, 0)                                           #Introduim el botó Clear a la part inferior de la capsa 
        self.clear_button.set_name("clear_button")                                                           #Assignem una ID al botó
       
    """
    Crea i arrenca el fil auxiliar.
    """
    def start_reading_thread(self):
        self.thread = threading.Thread(target=self.rf_reading_task)                                          #El thread un cop fem -start(), executarà la funció passada per argument
        self.thread.daemon = True                                                                            #Fa que el fil termini d'executar (encara que no hagui lleguit cap uid) si la finestra es tanca.
        self.thread.start()                                                                                  #Arrenquem el thread auxiliar
        
    """
    Funció que executarà el thread auxiliar. GTK no es thread-safe, per tant per evitar problemes hem de actualitzar la interfaç des de el fil principal, no desde el secundari. 
    """
    def rf_reading_task(self):
        self.myReader.read_uid()                                             #Executa el mètode del puzzle1 per tal d'obtenir el uid. Mètode bloquejant, però com és un Thread secundari la interfície no es veura afectada                 
        GLib.idle_add(self.update_window, self.myReader.uid)                 #El fil secundari farà que s'executi el mètode update_window des de el fil principal per actualitzar la interfaç de forma segura. Passem la uid com argument de la funció "update_window".

    """
    Iniciem tots els widgets i apliquem les regles CSS. Iniciem el thread auxiliar per llegir el carnet UPC i mostrem tots els widgets de la finestra.
    """
    def start_window(self):    
        self.start_boxes()
        self.start_labels()
        self.start_buttons()
        self.configure_style_CSS()                                                                          #Apliquem les regles CSS als widgets.
        self.start_reading_thread()                                                                         
        self.show_all()                                                                                     #Mostrem els widgets de la finestra.
   
    """
    Un cop es detecta una lectura, es modifica el label de benvinguda i es mostra el uid per pantalla.
    Paràmetres:
        :uid: Identificador de la tarjeta obtingut a la lectura.
    """
    def update_window(self,uid):
        self.welcome_label.set_name("accepted_label")		                                                 #Modifiquem la ID del label per aplicar-li altres regles CSS
        self.welcome_label.set_text(f"uid: {uid}")                                                           #Posem la uid detectada com el text del label.                                                                                     
        
    """
    Torna la finestra a l'estat inicial un cop polsem el botó "Clear".
    """    
    def reset_window(self,widget):
         self.welcome_label.set_name("welcome_label")	                                                     #Tornem a la configuració inicial                              
         self.welcome_label.set_text(WELCOME_STRING)                                                         #Tornem a posar el text de benvinguda
         self.myReader.uid = None                                                                            #Esborrem la uid prèvia
         self.start_reading_thread()                                                                         #Tornem a executar el fil secundari per poder tornar a lleguir una uid.      

    """
    Funció que aplica les regles CSS als widgets. El mètode set_widget_name realitzat sobre el label i els botons ho he fet per ara poder aplicar el selector #<widget> per tal d'aplicar regles CSS individuals a cada widget.
    """
    def configure_style_CSS(self):                                   
        
        self.editor_css.load_from_path("estils.css")                                                              #Carreguem les regles d'estil CSS del fitxer estils.css
        screen = Gdk.Screen.get_default()                                                                         #Obtenim una referència a la pantalla de la aplicació
        Gtk.StyleContext.add_provider_for_screen(screen,self.editor_css,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)  #Apliquem les regles CSS als widgets de la finestra.


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Classe que permet gestionar la aplicació principal, gestiona les finestres.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class Application(Gtk.Application):
    def __init__(self):
        super().__init__()         
    """
    Mètode que s'executa cuan es crida la funció .run() a un objecte d'aquesta mateixa classe.
    """
    def do_activate(self):       
        self.window = MyWindow()                                                         #Instanciem una finestra i passem un objecte widgetManager per paràmetre.
        self.window.configure_window(400,100,Gtk.WindowPosition.CENTER,"PUZZLE2")        #Configurem la finestra.
        self.window.connect("destroy", Gtk.main_quit)                                    #La finestra es podrà esborrar de forma manual eliminant la pestanya o clicant a la X.
        self.window.start_window()                                                       #Arranquem la finestra.
        self.window.present()                                                            #Mostrem la finestra.
        Gtk.main()                                                                       #Permet mantenir la finestra oberta i respondre a events com clicar un botó.


if __name__ == "__main__":        
       app = Application()                                                                #Instanciem un objecte de la classe Application
       app.run()                                                                          #Arrenquem la aplicació
    







