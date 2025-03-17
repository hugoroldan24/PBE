"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
En el puzzle2 es demana crear una versió gràfica del puzzle1. S'utilitzarà la la biblioteca PyGObject. PyGObject es un binding que permet utilitzar les llibreries basades en GObject com GTK3 que estàn escrites amb C però desde Python.
Per instalar aquesta biblioteca fem: sudo pip3 install PyGObject. Seguidament, descarreguem el paquet gtk3 que es el que conté les funcions per crear la interfaç. sudo apt install python3-gi (bindings de GTK para python, sudo apt install libgtk-3-dev. Finalment, instalem el paquet gir1.2-gtk-3.0. Aquest paquet permet a la llibreria PyGObject accedir a les funcionalitats de la llibreria gtk3 desde Python.
sudo apt install gir1.2-gtk-3.0
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import gi
import puzzle1 
import threading 
gi.require_version("Gtk", "3.0")                              #Indiquem que volem fer servir GTK3
from gi.repository import Gtk, GLib                           #Importem desde el repositori de gi la llibreria Gtk i GLib que conté les classes i mètodes per crear la interfaç i interactuar amb threads auxiliars respectivament. 

WELCOME_STRING = "Please, login with your university card"
GREEN_COLOR = Gdk.RGBA(0.0, 1.0, 0.0, 1.0)                    #Color verd en format RGBA (R=0, G=1, B=0, A=1)
BLUE_COLOR = Gdk.RGBA(0.0, 0, 1, 1.0)                         #Color blau en format RGBA (R=0, G=0, B=1, A=1)


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Classe per configurar la finestra d'una aplicació i els seus elements. La classe hereda la classe Gtk.ApplicationWindow
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class MyWindow(Gtk.ApplicationWindow):  
    """
    Inicialitza un objecte de la classe MyWindow.
    Paràmetres:
        :widgetManager: Objecte de la classe widgetManager per gestionar els widgets
    """
    def __init__(self,widgetManager):
        super().__init__()                                                 #Cridem a la funció __init__ de la classe Gtk.ApplicationWindow.
        self.wM = widgetManager                                 
        self.myReader = puzzle1.Rfid_522()                                 #Instancia un objecte de la classe Rfid_522() de la llibreria puzzle1.
      
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
        self.set_position(posició) 
      
    """
    Instancia totes les capses que es faràn servir, les configura i les afegeix a la finestra.
    """
    def start_boxes(self):            
        self.main_box = self.wM.create_box(Gtk.Orientation.VERTICAL,0)                                      #Creem una capsa amb orientació vertical
        self.add(main_box)                                                                                  #Afegim la capsa a la finestra
              
    """
    Instancia els labels que es faràn servir inicialment i els introdueix a la capsa principal
    """
    def start_labels(self):
        self.welcome_label = self.wM.create_label(WELCOME_STRING)                                            #Creem el label amb el text passat per paràmetre
        self.wM.add_widget_box_start(self.main_box,self.welcome_label, False, False, 0)                      #Afegim el label al inici de la capsa vertical (part superior)
        self.wM.set_widget_name(self.welcome_label,"welcome_label")                                          #Posem un nom al widget per tal de aplicar-li les regles CSS
      
    """
    Instancia els botons que es faràn servil inicialmente. Configura les seves característiques i els afegeix a la capsa
    """
    def start_buttons(self):
        self.exit_button = self.wM.create_button("Exit")                                                     #Creem el botó Exit.
        self.exit_button.connect("clicked",Gtk.main_quit)                                                    #Terminem la finestra quan pressionem el botó.
        self.wM.add_widget_box_end(self.main_box,self.exit_button, False, False, 0)                          #Afegim el botó al final de la capsa vertical (part inferior)
        self.wM.set_widget_name(self.exit_button,"exit_button")

        self.clear_button = self.wM.create_button("Clear")                                                   #Creem el botó Clear
        self.clear_button.connect("clicked",self.reset_window)                                               #S'executarà el mètode reset_window() quan es pressioni el botó "Clear"
        self.wM.add_widget_box_end(self.main_box,self.clear_button, False, False,0)                          #Introduim el botó Clear a la capsa 
        self.wM.set_widget_name(self.clear_button,"clear_button")        
        
    """
    Crea i arrenca el fil auxiliar.
    """
    def start_reading_thread(self):
        self.thread = threading.Thread(target=self.rf_reading_task)                                          #El thread executarà la funció passada per argument
        self.thread.daemon = True                                                                            #Fa que el fil termini d'executar (encara que no hagui lleguit cap uid) si la finestra es tanca.
        self.thread.start()                                                                                  #Arrenquem el thread auxiliar
        
    """
    Funció que executarà el thread auxiliar. GTK no es thread-safe, per tant per evitar problemes hem de actualitzar la interfaç des de el fil principal, no desde el secundari. 
    """
    def rf_reading_task(self):
        self.myReader.read_uid()                                             #Executa el mètode del puzzle1 per tal d'obtenir el uid                   
        GLib.idle_add(self.update_window, self.myReader.uid)                 #Fem es fer que el fil secundari faci que s'executi el mètode update_window des de el fil principal per actualitzar la interfaç de forma segura. Passem la uid com argument de la funció "update_window"

    """
    Iniciem tots els widgets i apliquem les regles CSS. Iniciem el thread auxiliar per llegir el carnet UPC i mostrem tots els widgets de la finestra.
    """
    def start_window(self):    
        self.start_boxes()
        self.start_labels()
        self.start_buttons()
        self.wM.configure_style_CSS()                                                                       #Apliquem totes les regles CSS als widgets
        self.start_reading_thread()                                                                          
        self.show_all()                                                                                     #Mostrem els widgets de la finestra
   
    """
    Un cop es detecta una lectura, es fa visible el botó "Clear", es modifica el label de benvinguda i es mostra el uid per pantalla.
    Paràmetres:
        :uid: Identificador de la tarjeta obtingut a la lectura.
    """
    def update_window(self,uid):
        self.wM.change_background_color(self.welcome_label,GREEN_COLOR)                                      #Posem el fons del label de color verd.
        self.welcome_label.set_text(f"uid: {uid}")                                                                                     
        
    """
    Torna la finestra a l'estat inicial un cop polsem el botó "Clear".
    """    
    def reset_window(self,clear_button):
         self.wM.change_background_color(self.welcome_label,BLUE_COLOR)                                      #Tornem a posar el fons blau al label
         self.welcome_label.set_text(WELCOME_STRING)                                                         #Tornem a posar el text de benvinguda
         self.myReader.uid = None                                                                            #Esborrem la uid prèvia
         self.start_reading_thread()                                                                         #Tornem a executar el fil secundari per poder tornar a lleguir una uid.
      
        
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Aquesta classe s'encarrega de fer una total gestió dels widgets. La seva funció es crear i modificar els widgets de la finestra.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class widgetManager:
    def __init__(self):         
        self.editor_css = Gtk.CssProvider()                                                                  #Creem l'objecte que controlarà les regles d'estil CSS.   
      
   """
   Crea un label.
   Paràmetres:
       :text: Text que es vol mostrar al label.
     Return:
       Label: Torna un label amb el text especificat
   """   
   def create_label(self,text):             
      return Gtk.Label(label=text)                                                                            #Creem un label i el retornem.
                  
    """
    Crea una capsa.
    Paràmetres:
        :orientation: Orientació de la capsa (horitzontal, vertical).
        :spacing: Quantitat d'espai que deixaran els widgets de la capsa entre ells.
     Return:
        Box: Torna una capsa amb els paràmetres especificats
    """
    def create_box(self,orientation,spacing): 
        return Gtk.Box(orientation=orientation,spacing=spacing)                                             #Creem la capsa i la retornem.
        
    """
    Crea un botó. 
    Paràmetres:
        :text: Text que contindrà el botó.
    Return:
        Button: Tornem un botó amb el text especificat
    """          
    def create_button(self,text):         
       return Gtk.Button(label=text)                                                                         #Creem el botó i el retornem         
            
    """
    Afegim el widget al inici de la capsa passada per argument.
    Paràmetres:    
        :box: Capsa a la qual volem afegir un widget.
        :widget: Widget que volem afegir a la capses.
        :expand(boolean): Si vols que el widget s'expandeixi per omplenar el espai lliure de la capsa, altrament, el widget mantindrà el seu tamany original.
        :fill(boolean): Si vols que el widget ompleni el espai disponible dintre de l'àrea que se li assgina a la capsa.
        :padding: Marge en píxels entre el widget i la capsa.
    """
    def add_widget_box_start(self,box,widget,expand,fill,padding):
        box.pack_start(widget, expand, fill, padding)
      
    """
    Afegim el widget al inici de la capsa passada per argument.
    Paràmetres:    
        :box: Capsa a la qual volem afegir un widget.
        :widget: Widget que volem afegir a la capses.
        :expand(boolean): Si vols que el widget s'expandeixi per omplenar el espai lliure de la capsa, altrament, el widget mantindrà el seu tamany original.
        :fill(boolean): Si vols que el widget ompleni el espai disponible dintre de l'àrea que se li assgina a la capsa.
        :padding: Marge en píxels entre el widget i la capsa.
    """  
    def add_widget_box_end(self,box,widget,expand,fill,padding):
        box.pack_end(widget, expand, fill, padding)
      
    """
    Configurem el nom del widget
    """
    def set_widget_name(self,widget,name)
        widget.set_name(name)
   
    """
    Funció que modifica el color de fons de un widget. És útil si volem modificar el color de forma dinàmica un cop ja hem aplicat les regles CSS
    Paràmetres:
        :widget: Widget que volem editar.
        :color: Color que volem introduir. Ha de ser un objecte de la glase Gtk.RGBA.
    """
    def change_backgroud_color(self,widget,color)
        widget.override_background_color(Gtk.StateFlags.NORMAL,color)
      
    """
    Funció que aplica les regles CSS als widgets.
    Paràmetres:
      
        :color_fons: Color desijat del fons del widget.
        :color_text: Color desijat del text del widget.
        :padding: Marge entre el text i la seva vora.
        :border_radius: Radi de curvatura de la vora del widget.
    """
    def configure_style_CSS(self):                                   
      css = b"""                                    #Creem la cadena de text que conté regles CSS dinàmicament utilitzant f-strings.                                                                         
        #welcome_label{
            background-color: blue;                 #Color desijat del fons del widget.                                                                                                                             
            color: white;                           #Color desijat del text del widget.                  
            padding: 60px;                          #Marge entre el text i la seva vora.            
            border-radius: 10px;                    #Radi de curvatura de la vora del widget.
            margin-left: 5px;                       #Marge esquerra
            margin-right: 5px;                      #Marge dret
            margin-top 5px;
            font-size: 20;                          #Tamany del text
            }
        #exit_button{
            background-color: #FF5959;  
            color: black;                  
            padding: 5px;                  
            border-radius: 10px;
            border: 2px dotted red;
            margin-left: 5px;
            margin-right: 5px;          
            margin-bottom: 5px;
            font-size: 20px;
            }
        #clear_button{
            background-color: #B4B1B2;  
            color: black;                  
            padding: 5px;
            border-radius: 10px;
            border: 2px dotted gray;
            margin-left: 5px;
            margin-right: 5px;
            margin-bottom: 5px;
            margin-top: 5px;
            font-size: 20px;
            }                        
         """
        self.editor_css.load_from_data(css)                                                                       #Carreguem les regles d'estil CSS del string "css" al proveïdor CSS que hem instanciat al mètode __init__.
        screen = Gdk.Screen.get_default()
        Gtk.StyleContext.add_provider_for_screen(screen,self.editor_css,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)  #Apliquem les regles CSS als widgets.


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
Classe que permet gestionar la aplicació principal, gestiona les finestres.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
class Application(Gtk.Application):
    def __init__(self):
        super().__init__()         
    """
    Mètode que s'executa cuan es crida la funció .run() a objecte d'aquesta mateixa classe.
    """
    def do_activate(self):       
        self.window = MyWindow(widgetManager())                                          #Instanciem una finestra i passem un objecte widgetManager per paràmetre.
        self.window.configure_window(400,300,Gtk.WindowPosition.CENTER,"PUZZLE2")        #Configurem la finestra.
        self.window.connect("destroy", Gtk.main_quit)                                    #La finestra es podrà esborrar de forma manual eliminant la pestanya o clicant a la X.
        self.window.start_window()                                                       #Arranquem la finestra.
        self.window.present()                                                            #Mostrem la finestra.
        Gtk.main()                                                                       #Permet mantenir la finestra oberta i respondre a event com clicar un botó.


if __name__ == "__main__":        
       app = Application()                                                                #Instanciem un objecte de la classe Application
       app.run()                                                                          #Arrenquem la aplicació
    







