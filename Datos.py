"""
Cada clase permite leer los archivos .txt de las palabras,
para poder instanciar los datos de manera mas rapida, cuándo
sean necesarios, según la partida
"""
class Data4:
    """
    clase para manejar los datos de las partidas que tienen palabras
    de un rango de 4 letras
    """
    def __init__(self,initial_data=None):
        if initial_data is None:
            initial_data=set()
        self.data=initial_data
    
    def words4(self):
        with open("palabras_validas4.txt","r") as archivo:
            for linea in archivo:
                palabra=linea.strip()
                self.data.add(palabra)
        
        return self.data
class Data5:
    """
    clase para manejar los datos de las partidas que tienen palabras
    de un rango de 5 letras
    """
    def __init__(self,initial_data=None):
        if initial_data is None:
            initial_data=set()
        self.data=initial_data

    def words5(self):
        with open("palabras_validas5.txt","r") as archivo:
            for linea in archivo:
                palabra=linea.strip()
                self.data.add(palabra)
        return self.data

class Data6:
    """
    clase para manejar los datos de las partidas que tienen palabras
    de un rango de 6 letras
    """
    def __init__(self,initial_data=None):
        if initial_data is None:
            initial_data=set()
        self.data=initial_data
   
    def words6(self):
        with open("palabras_validas6.txt","r") as archivo:
            for linea in archivo:
                palabra=linea.strip()
                self.data.add(palabra)
        
        return self.data

class Data7:
    """
    clase para manejar los datos de las partidas que tienen palabras
    de un rango de 7 letras
    """
    def __init__(self,initial_data=None):
        if initial_data is None:
            initial_data=set()
        self.data=initial_data
    def words7(self):
        with open("palabras_validas7.txt","r") as archivo:
            for linea in archivo:
                palabra=linea.strip()
                self.data.add(palabra)
        
        return self.data

class Data8:  
    """
    clase para manejar los datos de las partidas que tienen palabras
    de un rango de 8 letras
    """
    def __init__(self,initial_data=None):
        if initial_data is None:
            initial_data=set()
        self.data=initial_data  

    def words8(self):
        with open("palabras_validas8.txt","r") as archivo:
            for linea in archivo:
                palabra=linea.strip()
                self.data.add(palabra)
        
        return self.data
        
