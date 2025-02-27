"""
El primer puzzle consisteix en imprimir per consola el uid (user identifier) de la tarjeta o clauer Mifare S50 o la tarjeta de la UPC.
Utilitzaré la llibreria SimpleMFRC522 del paquet de llibreries mfrc522. 
Per instalarla, he fet servir la següent comanda a la terminal:
pip install mfrc522-python --break-system-packages
Descarrego la llibreria desde el repositori en linea de python PyPI. 
La informació de la llibrería ha sigut trobada a https://pypi.org/project/mfrc522-python/
""" 
from mfrc522 import SimpleMFRC522                     #Importo la llibreria SimpleMFRC522 del paquet mfrc522
class Rfid_522:
  """Mètode constructor que s'executa quan instanciem un objecte de la classe Rfid_522"""
  def __init__(self):
      self.uid = None                                  # Declarem l'atribut uid i l'inicializtem com a None 
      self.reader = SimpleMFRC522()                    # Instanciem un objecte de la clase SimpleMFRC522()
  """Mètode bloquejant (mètode read_id de la llibreria SimpleMFRC522 és bloquejant) que llegueix el uid i ho guarda en format hexadecimal a l'atribut "uid" de la pròpia classe"""
  def read_uid(self): 
      self.uid = hex(self.reader.read_id())[2:].upper()  # Utilitza el mètode read_id() de la llibreria SimpleMFRC522 sobre l'objecte reader que retorna l'id en format Integer. Després el convertim a hexadecimal, eliminem el prefixe "0x" i ho posem en majúscules amb el mètode upper(). 
if __name__ == "__main__":                             # Aquesta linea permet que el codi no s'executi automàticament si l'importem com a mòdul en un altre script (quan fem el puzzle2 per exemple). El codi només s'executarà quan l'executem directament escribint a la terminal: python puzzle1.py.
      rf = Rfid_522()                                  # Instancia un objecte de la classe Rfid_522()
      rf.read_uid()                                    # Obté el valor de l'uid en hexadecimal, que es guardarà a l'atribut uid. Com el mètode és bloquejant, no s'impimirà res fins que no apropem el clauer i obtenim una uid.
      print(f"uid:{rf.uid}")                          # Imprimeix l'identificador en format hexadecimal per pantalla


