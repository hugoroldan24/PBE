"""
En el puzzle2 es demana crear una versió gràfica del puzzle1. S'utilitzarà la la biblioteca PyGObject. PyGObject es un binding que permet utilitzar les llibreries basades en GObject com GTK3 que estàn escrites amb C però desde Python.
Per instalar aquesta biblioteca fem: sudo pip3 install PyGObject. Seguidament, descarreguem el paquet gtk3 que es el que conté les funcions per crear la interfaç. sudo apt install libgtk-3-dev. Finalment, instalem el paquet gir1.2-gtk-3.0. Aquest paquet permet a la llibreria PyGObject accedir a les funcionalitats de la llibreria gtk3 desde Python.
sudo apt install gir1.2-gtk-3.0-

"""
import gi
import puzzle1 
import threading 
gi.require_version("Gtk", "3.0")                              #Indiquem que volem fer servir GTK3
from gi.repository import Gtk, GLib                           #Importem desde el repositori de gi la llibreria Gtk i GLib que conté les classes i mètodes per crear la interfaç i interactuar amb threads auxiliars respectivament. 

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
        super().__init__()                                    #Truquem a la funció __init__ de la classe Gtk.ApplicationWindow.
        self.wM = widgetManager()                             #Instanciem un objecte de la clase widgetManager, s'encarregarà de gestionar tot lo relacionat amb els wadgets.
        self.myReader = Rfid_522()                                 # Instancia un objecte de la classe Rfid_522() de la llibreria puzzle1.
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
    Per tal de distribuir les capses de forma que quedi una a sobre de la altre, creo una capsa vertical i considero la capsa inferior i superior com si fossing wadgets. 
    Si configuro que la caixa superior tingui els paràmetrs expand i fill com a True i la inferior com a False, en l'ordre que s'executa el codi, quedaràn col·locades com s'espera.
    La capsa inferior contindrà els botons de Sortir i Clear, la superior els labels de text.
    """
    def start_boxes(self):     
        self.wM.create_box(Gtk.Orientation.HORIZONTAL,0)                                  #Creem la capsa 0 (inferior).
        self.wM.create_box(Gtk.Orientation.HORIZONTAL,0)                                  #Creem la capsa 1 (superior).
        self.wM.create_box(Gtk.Orientation.VERTICAL,0)                                    #Creem la capsa 2 (conté les capses 0 i 1).
        self.wM.add_widget_box(self.wM.boxes[2],self.wM.boxes[1],True,True,0)              #Afegim la capsa 1 (superior) a la capsa 2 (principal).
        self.wM.add_widget_box(self.wM.boxes[2],self.wM.boxes[0],False,False,0)            #Afegim la capsa 0 (inferior) a la capsa 2 (principal).
        self.add(self.wM.boxes[2])                                                        #Afegim la capsa principal a la finestra, aquesta capsa conté tots els wadgets.
    """
    Instancia els labels que es faràn servir inicialment. També configura les seves característiques i les afegeix a la Capsa 1.
    """
    def start_labels(self):
        self.wM.create_label(""""                    Benvingut!                            
                                          Siusplau, identifique-vos apropant el vostre carnet de la UPC """)
        self.wM.configure_style(self.wM.labels[0],"#4682B4","black","0","0")                               #Configurem l'estil del Label de benvinguda.
        self.wM.add_widget_box(self.wM.boxes[1],self.wM.labels[0],True,True,0)                             #Afegim el label de benvinguda a la capsa 1 (superior).
    """
    Instancia els botons que es faràn servil inicialmente. Configura les seves característiques i els afegeix a la Capsa 0.
    """
    def start_buttons(self):
        self.wM.create_button("Surt")                                                       #Creem el botó de sortida.
        self.wM.buttons[0].connect("clicked",self.exit_button_pressed)                      #S'executarà la funció "exit_buttom_pressed quan pressionem el botó.
        self.wM.configure_style(self.wM.buttons[0],"red","black","0","20")                  #Configurem l'estil del botó de sortida.
        self.wM.buttons[0].set_halign(Gtk.Align.START)                                      #Situem el botó de sortida a la esquerra de la caixa.
        self.wM.add_widget_box(self.wM.boxes[0],self.wM.buttons[0],False,False,0)           #Afegim el botó "Surt" a la capsa 0 (inferior).
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
        self.thread.start()
        
    """
    Funció que executarà el thread auxiliar. GTK no es thread-safe, per tant per evitar problemes hem de actualitzar la interfaç des de el fil principal, no desde el secundari.
    """
    def rf_reading_task(self):
        self.myReader.read_uid()                                        #Executa el mètode del puzzle1 per tal d'obtenir el uid                   
        GLib.idle_add(self.update_window, myReader.uid)                 #El que fem es fer que el fil secundari faci que s'executi el mètode update_window des de el fil principal per actualitzar la interfaç de forma segura. Passem també la uid com argument
   
    """
    Un cop es detecta una lectura, es crea el botó "Clear", es modifica el label de la capsa 1 i es mostra el uid per pantalla.
    Paràmetres:
        :uid: Identificador de la tarjeta obtingut a la lectura.
    """
    def update_window(self,uid):
        self.wM.configure_style(self.wM.labels[0],"green","black","0","0")
        self.wM.labels[0].set_text(f"""                    Tarjeta detectada satisfactòriament!
                                                                     uid: {uid}""")
        self.wM.create_button("Clear")                                               #Creem el botó "Clear", aquest es guardarà a la posició 1 del vector de botons del objecte de la classe widgetManager
        self.wM.configure_style(self.wM.buttons[1],"gray","black","0","20")
        self.wM.add_widget_box(self.wM.boxes[0],self.wM.buttons[1],False,False,0)    #Introduim el botó Clear a la capsa 0 (inferior)
        self.wM.buttons[1].set_halign(Gtk.Align.CENTER)                              #Col·loquem el botó al centre de la capsa
        self.wM.buttons[1].connect("clicked",self.reset_window)                      #S'executarà el mètode reset_window() quan es pressioni el botó "Clear"
         
    """
    Torna la finestra a l'estat inicial un cop polsem el botó "Clear".
    """    
    def reset_window(self):
         self.wM.configure_style(self.wM.labels[0],"blue","black","0",0")
         self.wM.labels[0].set_text(f"""""""                    Benvingut!
                                          Siusplau, identifique-vos apropant el vostre carnet de la UPC """)
         self.wM.buttons[1].destroy()
         self.thread.start()

"""
Aquesta classe s'encarrega de fer una total gestió dels widgets. La seva funció es crear, modificar i emmagetzemar els widgets segons com l'objecte de la classe MyWindow demani.
S'ha de considerar que al executar els mètodes per crear widgets i afegirlos als seus respectius vectors, aquests estaran ordenats al vector de widgets segons l'ordre de crida del seu mètode de creació. 
Per exemple, si es crida primer 'create_label(String1)' i seguidament 'create_label(String2)', el label String1 es guardarà a labels[0] o String2 a labels[1], però si executes primer 'create_label(String2)' i després
'create_label(String1)', l'ordre al vector labels[] s'haurà invertit.
"""
class widgetManager:
        """
        Instancia un objecte de la classe widggetManager. Crea els vectors que contindran les capses, botons i labels que es vaguin creant.
        """
        def __init__(self):
            self.boxes = []
            self.buttons = []
            self.labels = []
            editor_css = Gtk.CssProvider()                             #Creem l'objecte que controlarà les regles d'estil CSS.      
        
        """
        Crea un label.
        Paràmetres:
            :text: Text que es vol mostrar al label.
        """   
        def create_label(self,text):
            self.labels.append(Gtk.Label(label=text))                   #Guardem el label al vector labels[] de la classe.
        
        """
        Crea una capsa.
        Paràmetres:
            :orientation: Orientació de la capsa (horitzontal, vertical).
            :spacing: Quantitat d'espai que deixaran els widgets de la capsa entre ells.
        """
        def create_box(self,orientation,spacing):
            box = Gtk.Box(orientation=orientation,spacing=spacing)
            self.boxes.append(box)                                      #Guardem la capsa al vector boxes[] de la classe.
        
        """
        Crea un botó.
        Paràmetres:
            :text: Text que contindrà el botó.
        """          
        def create_button(self,text):                        
            self.botons.append(Gtk.Button(label=text))                 #Guardem el botó al vector buttons[] de la classe.         
            
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
            self.editor_css.load_from_data(css.encode())                                         #Carreguem les regles d'estil CSS del string "css" en format de bytes al proveïdor CSS que hem instanciat al mètode __init__.
            style_context = widget.get_style_context()                                           #Obtenim accés a la informació del stil del widget per poder modificarl-lo.
            style_context.add_provider(self.editor_css,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)  #Editem el stil del widget amb les caràcteristiques carregades al objecte editor_css.

        """
Classe que permet gestionar les finestres
"""
class Application(Gtk.Application):
    def __init__(self):
        super().__init__()
    """
    Mètode que s'executa cuan es crida la funció .run() a objecte d'aquesta mateixa classe.
    """
    def do_activate(self):
        window = myWindow(widgetManager())                 #Instanciem una finestra i passem un objecte widgetManager per paràmetre.
        window.configure_window(400,300,Gtk.WindowPosition.CENTER,"PUZZLE2")        #Configurem la finestra.
        win.connect("destroy",self.quit)                   #La finestra es podrà esborrar de forma manual eliminant la pestanya o clicant a la X.
        window.start_window()                              #Arranquem la finestra.
        window.present()                                   #Mostrem la finestra.
                                                                        
if __name__ == "__main__":        
      app = Application()                                   #Instanciem un objecte de la classe Application
      app.run()                                             #Arrenquem la aplicació
    







