"""
En el puzzle2 es demana crear una versió gràfica del puzzle1. S'utilitzarà la la biblioteca PyGObject. PyGObject es un binding que permet utilitzar les llibreries basades en GObject com GTK3 que estàn escrites amb C però desde Python.
Per instalar aquesta biblioteca fem: sudo pip3 install PyGObject. Seguidament, descarreguem el paquet gtk3 que es el que conté les funcions per crear la interfaç. sudo apt install libgtk-3-dev. Finalment, instalem el paquet gir1.2-gtk-3.0. Aquest paquet permet a la llibreria PyGObject accedir a les funcionalitats de la llibreria gtk3 desde Python.
sudo apt install gir1.2-gtk-3.0

"""
import gi
import puzzle1 
import threading 
gi.require_version("Gtk", "3.0")                          #Indiquem que volem fer servir GTK3
from gi.repository import Gtk, GLib                             #Importem desde el repositori de gi la llibreria Gtk que conté les classes y mètodes per crear la interfaç. 

class MyWindow(Gtk.Window):  #Clase relacionada amb la finestra de la aplicació. La classe hereda la clase Gtk.Window de gtk3
    def __init__(self,widgetManager,widgetEditor):
        super().__init__()                                 #Truquem a la funció __init__ de la classe Gtk.Window     
        self.wM = widgetManager()                            #Instanciem un objecte de la clase widgetManager, s'encarregarà de gestionar tot lo relacionat amb els wadgets
        myReader = Rfid_522()                                  # Instancia un objecte de la classe Rfid_522() de la llibreria puzzle1  
    def configure_window(self,amplada,altura,posició,titol):
        self.set_title(titol) 
        self.set_default_size(amplada,altura)
        self.set_position(posició) 
        
    def start_boxes(self)
          """Per tal de distribuir les capses de forma que quedi una a sobre de la altre, creo una capsa vertical i considero la capsa inferior i superior com si fossing wadgets. 
        Si configuro que la caixa superior tingui els paràmetrs expand i fill com a True i la inferior com a False, en l'ordre que s'executa el codi quedaràn col·locades com s'espera"""
        
        self.wM.create_box(Gtk.Orientation.HORIZONTAL,0)                                  #Creem la capsa 0 (inferior)
        self.wM.create_box(Gtk.Orientation.HORIZONTAL,0)                                  #Creem la capsa 1 (superior)
        self.wM.create_box(Gtk.Orientation.VERTICAL,0)                                    #Creem la capsa 2 (conté les capses 0 i 1)

        self.wM.add_widget_box(self.wM.boxes[2],self.wM.boxs[1],True,True,0)             #Afegim la capsa 1 (superior) a la capsa 2 (principal)
        self.wM.add_widget_box(self.wM.boxes[2],self.wM.boxs[0],False,False,0)           #Afegim la capsa 0 (inferior) a la capsa 2 (principal)

        self.add(self.wM.boxes[2])                                                          #Afegim la capsa principal a la finestra, aquesta capsa conté tots els wadgets    

    def start_labels(self)
        self.wM.create_label(""""                    Benvingut!
                                          Siusplau, identifique-vos apropant el vostre carnet de la UPC """)
        self.wE.configure_style(self.wM.labels[0],"#4682B4","black","0","0")               #Configurem l'estil del Label de benvinguda
        self.wM.add_widget_box(self.wM.boxes[1],self.wM.labels[0],True,True,0)             #Afegim el label de benvinguda a la capsa 1 (superior)
        
    def start_buttons(self)
        self.wM.create_button("Surt")                                                      #Creem el botó de sortida
        self.wM.buttons[0].connect("clicked",self.exit_buttom_pressed)                     #S'executarà la funció "exit_buttom_pressed quan pressionem el botó
        self.wM.configure_style(self.wM.buttons[0],"red","black","0","20")                 #Configurem l'estil del botó de sortida
        self.wM.buttons[0].set_halign(Gtk.Align.START)                                     #Situem el botó de sortida a la esquerra de la caixa
        self.wM.add_widget_box(self.wM.boxs[0],self.wM.buttons[0],False,False,0)           #Afegim el botó "Surt" a la capsa 0 (inferior)
        
     def start_window(self):    
        self.start_boxes()
        self.start_labels()
        self.start_buttons()
        self.show_all()
         
    def exit_button_pressed(self):
        Gtk.main_quit()
        
    def rf_reading_task(self)
        self.myReader.read_uid()     
        GLib.idle_add(self.update_window, myReader.uid)                # GTK no es thread-safe, per tant per evitar problemes hem de actualitzar la interfaç des de el fil principal, no desde el secundari.
                                                                        #El que fem es fer que el fil secundari faci que s'executi el mètode update_window des de el fil principal
        
    def update_window(self,uid)

    def start_reading_thread(self)
        thread = threading.Thread(target=self.rf_reading_task)
        
class widgetManager:
    def __init__(self):
        self.boxes = []
        self.buttons = []
        self.labels = []
        editor_css = Gtk.CssProvider()                                                       #Creem l'objecte que controlarà les regles d'estil CSS
    def create_label(self,text):
        self.labels.append(Gtk.Label(label=text))
        
    def create_box(self,orientation,spacing):
        box = Gtk.Box(orientation=orientation,spacing=spacing)
        self.boxes.append(box)
               
    def create_button(self,text):
        self.botons.append(Gtk.Button(label=text))
        
    def add_widget_box(self,box,widget,expand,fill,padding):
        box.pack_start(widget, expand, fill, padding)  
    def configure_style(self,widget,color_fons,color_text,padding,border_radius)
        css = f"""
        *{{
            background-color: {color_fons};  
            color: {color_text};                  
            padding: {padding}px;                  
            border-radius: {border_radius}px;   
        }}
        """
        self.editor_css.load_from_data(css.encode())
        style_context = widget.get_style_context()
        style_context.add_provider(self.editor_css,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        
                                                    
                    
if __name__ == "__main__":
      window = MyWindow(widgetManager())
      window.configure_window(400,300)
      win.connect("destroy", Gtk.main_quit)
      window.start_window()
      Gtk.main()
    







