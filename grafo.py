import random

class Grafo:
    ''' Representa un grafo. Está implementado como lista de adyacencias (diccionario de diccionarios) '''
    def __init__(self, dirigido = False):
        ''' Constructor de la clase grafo, recibe un booleano, false por default, si es o no dirigido '''
        self.vertices = {}
        self.dirigido = dirigido
    
    def agregar_vertice(self, clave):
        ''' Agrega un vértice nuevo al grafo, devuelve True si el vértice no existía en el grafo, False
            en caso contrario '''
        if clave not in self.vertices:
            self.vertices[clave] = {}
            return True
        return False

    def agregar_arista(self, desde, hasta, peso = 1):
        ''' Recibe dos vértices y el peso, 1 por default, y agrega una arista desde el primer vértice hasta el segundo con el peso indicado.
            Devuelve True si la arista no existía, False en caso contrario '''
        if desde in self.vertices and hasta in self.vertices:
            self.vertices[desde][hasta] = peso
            if not self.dirigido: self.vertices[hasta][desde] = peso
            return True
        return False


    def borrar_vertice(self, clave):
        ''' Borra un vértice del grafo, devuelve True si se pudo borrar, es decir, si existía el vértice
            en el grafo, False en caso contrario '''
        if clave in self.vertices:     
            self.vertices.pop(clave)
            for k in self.vertices:
                if clave in self.vertices[k]:
                    self.vertices[k].pop(clave)
            return True
        return False


    def borrar_arista(self, desde, hasta):
        ''' Borra una arista del grafo, devuelve el peso de dicha arista, o None si la arista no existía '''
        if self.estan_unidos(desde, hasta):
            if not self.dirigido: self.vertices[hasta].pop(desde) 
            return self.vertices[desde].pop(hasta)
        return None 
    
    def estan_unidos(self, desde, hasta):
        ''' Devuelve True si los vértices están unidos mediante una arista, False en caso contrario '''
        return desde in self.vertices and hasta in self.vertices[desde]

    def peso(self, desde, hasta):
        ''' Recibe dos vértices y devuelve el peso de la arista que los conecta, None si no existe la arista '''
        if self.estan_unidos(desde, hasta):
            return self.vertices[desde][hasta]
        return None

    def vertice_random(self): 
        ''' Devuelve un vértice aleatorio del grafo, None en caso de un grafo vacío '''
        try: 
            return random.choice(list(self.vertices.keys()))
        except: 
            return None
    

    def obtener_vertices(self):
        ''' Devuelve un set con todos los vértices del grafo '''
        res = set()
        for clave in self.vertices:
            res.add(clave)
        return res

    def adyacentes(self, clave):
        ''' Devuelve un set con los vértices adyacentes al vértice recibido por parámetro '''
        res = set()
        if clave in self.vertices:
            for k in self.vertices[clave]:
                res.add(k)
        return res

    def __contains__(self, clave):
        ''' Método contains del grafo, devuelve True si la clave recibida está en el grafo, False en caso contrario '''
        return clave in self.vertices

    def __len__(self):
        ''' Método len del grafo, devuelve la cantidad de vértices '''
        return len(self.vertices)

    def __iter__(self): 
        ''' Devuelve un iterador para el grafo '''
        return _Iterador_Grafo(self)
        
class _Iterador_Grafo:
    ''' Representa un iterador para la clase grafo '''
    def __init__(self, grafo):
        ''' Constructor de la clase, recibe el grafo a iterar '''
        self.vertices = list(grafo.obtener_vertices())
        self.contador = 0
        self.cant_vertices = len(self.vertices)
    
    def __next__(self):
        ''' Avanza una vez la iteración sin un orden específico '''
        if (self.contador < self.cant_vertices):
            self.contador += 1
            return self.vertices[self.contador-1]
        raise StopIteration
