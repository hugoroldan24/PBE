"""
En el puzzle2 es demana crear una versió gràfica del puzzle1. S'utilitzarà la la biblioteca PyGObject. PyGObject es un binding que permet utilitzar les llibreries basades en GObject com GTK3 que estàn escrites amb C però desde Python.
Per instalar aquesta biblioteca fem: sudo pip3 install PyGObject. Seguidament, descarreguem el paquet gtk3 que es el que conté les funcions per crear la interfaç. sudo apt install python3-gi (bindings de GTK para python, sudo apt install libgtk-3-dev. Finalment, instalem el paquet gir1.2-gtk-3.0. Aquest paquet permet a la llibreria PyGObject accedir a les funcionalitats de la llibreria gtk3 desde Python.
sudo apt install gir1.2-gtk-3.0-

"""
import gi
import puzzle1 
import threading 
gi.require_version("Gtk", "3.0")                              #Indiquem que volem fer servir GTK3
from gi.repository import Gtk, GLib                           #Importem desde el repositori de gi la llibreria Gtk i GLib que conté les classes i mètodes per crear la interfaç i interactuar amb threads auxiliars respectivament. 

WELCOME_STRING = """                    Benvingut!                            
                                          Siusplau, identifique-vos apropant el vostre carnet de la UPC """
"""
Classe per configurar la finestra d'una aplicació i els seus elements. La classe hereda la classa Gtk.ApplicationWindow
"""
class MyWindow(Gtk.ApplicationWindow):  
    """
    Inicialitza un objecte de la classe MyWindow.
    Paràmetres:
        :widgetManager: Objecte de la classe widgetManager per gestionar els widgets
    """
    def __init__(self,widgetManager):
        super().__init__()                                         #Truquem a la funció __init__ de la classe Gtk.ApplicationWindow.
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
    Per tal de distribuir les capses de forma que quedi una a sobre de la altre, creo una capsa vertical i considero la capsa inferior i superior com si fossing widgets. 
    Si configuro que la caixa superior tingui els paràmetres expand i fill com a True i la inferior com a False, en l'ordre que s'executa el codi, quedaràn col·locades com s'espera.
    La capsa inferior contindrà els botons de Sortir i Clear, la superior els labels de text.
    """
    def start_boxes(self):     
        self.lower_box = self.wM.create_box(Gtk.Orientation.HORIZONTAL,0)                                  #Creem la capsa inferior que contindrà els butons
        self.upper_box = self.wM.create_box(Gtk.Orientation.HORIZONTAL,0)                                  #Creem la capsa superior que contindrà el label de text.
        self.main_box = self.wM.create_box(Gtk.Orientation.VERTICAL,0)                                     #Creem la capsa principal (conté les capses superior i inferior).
        self.wM.add_widget_box(self.main_box,self.upper_box,True,True,0)                                   #Afegim la capsa superior a la capsa principal.
        self.wM.add_widget_box(self.main_box,self.lower_box,False,False,0)                                 #Afegim la capsa inferior a la capsa principal.
        self.add(self.main_box)                                                                            #Afegim la capsa principal a la finestra, aquesta capsa conté tots els widgets.
    """
    Instancia els labels que es faràn servir inicialment. També configura les seves característiques i les afegeix a la capsa superior.
    """
    def start_labels(self):
        self.welcome_label = self.wM.create_label(WELCOME_STRING)
        self.wM.configure_style(self.welcome_label,"#4682B4","black","0","0")                                 #Configurem l'estil del Label de benvinguda.
        self.wM.add_widget_box(self.wM.boxes[1],self.welcome_label,True,True,0)                               #Afegim el label de benvinguda a la capsa superior.
    """
    Instancia els botons que es faràn servil inicialmente. Configura les seves característiques i els afegeix a la Capsa 0.
    """
    def start_buttons(self):
        self.exit_button = self.wM.create_button("Surt")                                                       #Creem el botó de sortida.
        self.exit_button.connect("clicked",self.exit_button_pressed)                                           #S'executarà la funció "exit_buttom_pressed" quan pressionem el botó.
        self.wM.configure_style(self.exit_button,"red","black","0","20")                                       #Configurem l'estil del botó de sortida.
        self.exit_button.set_halign(Gtk.Align.START)                                                           #Situem el botó de sortida a la esquerra de la caixa.
        self.wM.add_widget_box(self.lower_box,self.exit_button,False,False,0)                                  #Afegim el botó "Surt" a la capsa inferior.
    """
    Executem els 3 mètodes anterior. Iniciem el thread auxiliar per llegir el carnet UPC i mostrem tots els widgets de la finestra.
    """
    def start_window(self):    
        self.start_boxes()
        self.start_labels()
        self.start_buttons()
        self.start_reading_thread()
        self.show_all()
    """
    Termina la finestra un cop es pressiona el botó "Surt".
    """
    def exit_button_pressed(self):
        Gtk.main_quit()
        
    """
    Crea i arrenca el fil auxiliar.
    """
    def start_reading_thread(self):
        self.thread = threading.Thread(target=self.rf_reading_task)          #El thread executarà la funció passada per argument
        self.thread.daemon = True                                            #Fa que el fil termini d'executar (encara que no hagui lleguit cap uid) si la finestra es tanca.
        self.thread.start()
        
    """
    Funció que executarà el thread auxiliar. GTK no es thread-safe, per tant per evitar problemes hem de actualitzar la interfaç des de el fil principal, no desde el secundari. 
    """
    def rf_reading_task(self):
        self.myReader.read_uid()                                             #Executa el mètode del puzzle1 per tal d'obtenir el uid                   
        GLib.idle_add(self.update_window, self.myReader.uid)                 #El que fem es fer que el fil secundari faci que s'executi el mètode update_window des de el fil principal per actualitzar la interfaç de forma segura. Passem la uid com argument de la funció "update_window"
   
    """
    Un cop es detecta una lectura, es crea el botó "Clear", es modifica el label de la capsa superior i es mostra el uid per pantalla.
    Paràmetres:
        :uid: Identificador de la tarjeta obtingut a la lectura.
    """
    def update_window(self,uid):
        self.wM.configure_style(self.welcome_label,"green","black","0","0")
        self.welcome_label.set_text(f"""                    Tarjeta detectada satisfactòriament!
                                                                     uid: {uid}""")
        self.clear_button = self.wM.create_button("Clear")                                               #Creem el botó "Clear", aquest es guardarà a la posició 1 del vector de botons del objecte de la classe widgetManager
        self.wM.configure_style(self.clear_button,"gray","black","0","20")                               #Editem l'estil del botó Clear
        self.wM.add_widget_box(self.upper_box,self.clear_button,False,False,0)                           #Introduim el botó Clear a la capsa inferior
        self.clear_button.set_halign(Gtk.Align.CENTER)                                                   #Col·loquem el botó al centre de la capsa
        self.clear_button.connect("clicked",self.reset_window)                                           #S'executarà el mètode reset_window() quan es pressioni el botó "Clear"
         
    """
    Torna la finestra a l'estat inicial un cop polsem el botó "Clear".
    """    
    def reset_window(self):
         self.wM.configure_style(self.welcome_label,"#4682B4","black","0","0")
         self.welcome_label.set_text(WELCOME_STRING)
         self.clear_button.destroy()                                                                        #Eliminem el botó clear
         self.myReader.uid = None                                                                           #Esborrem la uid prèvia
         self.start_reading_thread()                                                                               #Tornem a executar el fil secundari per poder tornar a lleguir una uid.
        

"""
Aquesta classe s'encarrega de fer una total gestió dels widgets. La seva funció es crear i modificar els widgets segons com l'objecte de la classe MyWindow demani.
"""
class widgetManager:
        """
        Instancia un objecte de la classe widggetManager. 
        """
        def __init__(self):         
            self.editor_css = Gtk.CssProvider()                             #Creem l'objecte que controlarà les regles d'estil CSS.             
        """
        Crea un label.
        Paràmetres:
            :text: Text que es vol mostrar al label.
        Return:
            Label: Returns a label with the specified text
        """   
        def create_label(self,text):
          return Gtk.Label(label=text)                               #Creem un label i el retornem.
        
        """
        Crea una capsa.
        Paràmetres:
            :orientation: Orientació de la capsa (horitzontal, vertical).
            :spacing: Quantitat d'espai que deixaran els widgets de la capsa entre ells.
        Return:
            Box: Returns a box with the specified parameters
        """
        def create_box(self,orientation,spacing): 
            return Gtk.Box(orientation=orientation,spacing=spacing)                                     #Creem la capsa i la retornem.
        
        """
        Crea un botó.
        Paràmetres:
            :text: Text que contindrà el botó.
        Return:
            Button: Returns a button with the specified text
        """          
        def create_button(self,text):                        
          return Gtk.Button(label=text)                #Creem el botó i el retornem         
            
        """
        Afegim el widget a la capsa passada per argument.
        Paràmetres:    
            :box: Capsa a la qual volem afegir un widget.
            :widget: Widget que volem afegir a la capses.
            :expand(boolean): Si vols que el widget s'expandeixi per omplenar el espai lliure de la capsa, altrament, el widget mantindrà el seu tamany original.
            :fill(boolean): Si vols que el widget ompleni el espai disponible dintre de l'àrea que se li assgina a la capsa.
            :padding: Marge en píxels entre el widget i la capsa.
        """
        def add_widget_box(self,box,widget,expand,fill,padding):
            box.pack_start(widget, expand, fill, padding)  
        
        """
        Utilitzem el llenguatge CSS per editar els widgets.
        Paràmetres:
            :widget: Widget que volem editar.
            :color_fons: Color desijat del fons del widget.
            :color_text: Color desijat del text del widget.
            :padding: Marge entre el text i la seva vora.
            :border_radius: Radi de curvatura de la vora del widget.
        """
        def configure_style(self,widget,color_fons,color_text,padding,border_radius):
                                                                                                   #Creem la cadena de text que conté regles CSS dinàmicament utilitzant f-strings.
            css = f"""                                                                         
            *{{
                background-color: {color_fons};  
                color: {color_text};                  
                padding: {padding}px;                  
                border-radius: {border_radius}px;   
            }}
        """
            self.editor_css.load_from_data(css.encode())                                              #Carreguem les regles d'estil CSS del string "css" en format de bytes al proveïdor CSS que hem instanciat al mètode __init__.
            self.style_context = widget.get_style_context()                                           #Obtenim accés a la informació del stil del widget per poder modificarl-lo.
            self.style_context.add_provider(self.editor_css,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)  #Editem el stil del widget amb les caràcteristiques carregades al objecte editor_css.

"""
Classe que permet gestionar la aplicació principal, gestiona les finestres. En aquest cas només hem de gestiona una finestra.
"""
class Application(Gtk.Application):
    def __init__(self):
        super().__init__()         
    """
    Mètode que s'executa cuan es crida la funció .run() a objecte d'aquesta mateixa classe.
    """
    def do_activate(self):       
        self.window = MyWindow(widgetManager())                                          #Instanciem una finestra i passem un objecte widgetManager per paràmetre.
        self.window.configure_window(400,300,Gtk.WindowPosition.CENTER,"PUZZLE2")        #Configurem la finestra.
        self.window.connect("destroy",self.quit)                                         #La finestra es podrà esborrar de forma manual eliminant la pestanya o clicant a la X.
        self.window.start_window()                                                       #Arranquem la finestra.
        self.window.present()                                                            #Mostrem la finestra.
                                                                        
if __name__ == "__main__":        
      app = Application()                                                                #Instanciem un objecte de la classe Application
      app.run()                                                                          #Arrenquem la aplicació
    







