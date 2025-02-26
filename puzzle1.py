"""
El primer puzzle consisteix en imprimir per consola el uid (user identifier) de la tarjeta o clauer Mifare S50 o la tarjeta de la UPC.
Utilitzaré la llibreria SimpleMFRC522 del paquet de llibreries mfrc522. 
Per instalarla, he fet servir la següent comanda a la terminal:
pip install mfrc522-python 
Descarrego la llibreria desde el repositori en linea de python PyPI. Aquesta llibreria et fa interactuar amb el mòdul des de un nivell molt alt, però per l'aplicació demanada no és necessari programar-ho a un nivell més baix.
""" 
from mfrc522 import SimpleMFRC522                #Importo la llibreria SimpleMFRC522 del paquet mfrc522
class Rfid_522:
  """Mètode constructor que s'executa quan instanciem un objecte de la classe Rfid_522"""
  def __init__(self):
      self.uid = None                            # Declarem l'atribut uid i l'inicializtem com a None 
      self.reader = SimpleMFRC522()              # Instanciem un objecte de la clase SimpleMFRC522()
  """Llegueix el uid i ho guarda en format hexadecimal a l'atribut "uid" de la pròpia classe"""
  def read_uid(self): 
      self.uid = hex(self.reader.read_id())[2:]  # Utilitzem el mètode read_id() de la llibreria SimpleMFRC522 sobre l'objecte reader que retorna l'id en format Integer. Després el convertim a hexadecimal i eliminem el prefixe "0x". 
if __name__ == "__main__":                       # Aquesta linea permet que el codi no s'executi automàticament si l'importem com a mòdul en un altre script. El codi només s'executarà quan el fem correr directament escribint a la terminal python puzzle1.py.
      rf = Rfid_522()
      rf.read_uid()                              # Obtenim el valor de l'uid en hexadecimal, que es guardarà a l'atribut uid.
      print(f"uid: {rf.uid}")                    # Imprimim l'identificador en format hexadecimal per pantalla


