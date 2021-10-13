from grafo import Grafo
from collections import deque
import heapq
import random

D = 0.85
K = 20
ROJO = '\033[91m'
VERDE = '\033[92m'
AMARILLO = '\033[93m'
BLANCO = '\033[0m'

# -------------------------------------------------------------------- #
#                       COEFICIENTE DE CLUSTERING                      #
# -------------------------------------------------------------------- #

def coeficiente_de_clustering(grafo, v):
    ''' Calcula el coeficiente de clustering para un vértice recibido '''
    grado_v = 0
    vecinos = 0
    adyacentes_v = grafo.adyacentes(v)
    for w in adyacentes_v:
        grado_v += 1
        if w == v: continue
        for x in grafo.adyacentes(w):
            if x == w: continue
            if x in adyacentes_v:
                vecinos += 1
    denominador = (grado_v * grado_v) - grado_v
    return 0 if denominador == 0 else (vecinos / denominador)

def cdc_promedio(grafo):
    ''' Calcula el coeficiente de clustering de cada vértice y devuelve el promedio de todo el grafo ''' 
    cdc_total = 0
    cant_v = 0
    for v in grafo.obtener_vertices():
        cdc_total += coeficiente_de_clustering(grafo, v)
        cant_v += 1
    return cdc_total / cant_v


# -------------------------------------------------------------------- #
#                           RECORRIDOS CON BFS                         #
# -------------------------------------------------------------------- #

def bfs_rango(grafo, origen, n):
    ''' Recibe el grafo, un vértice de origen y un rango n, y devuelve la cantidad de vértices
        que se encuentran a distancia n del origen '''
    contador = 0
    visitados = set()
    visitados.add(origen)
    orden = {}
    orden[origen] = 0
    q = deque()
    q.appendleft(origen)
    while (q):
        v = q.pop()
        for w in grafo.adyacentes(v):
            if w in visitados: continue
            visitados.add(w)
            orden[w] = orden[v] + 1
            if orden[w] == n:
                contador += 1
            if orden[w] > n:
                break
            q.appendleft(w)
    return contador
                


def bfs(grafo, origen, destino):
    ''' Recorrido BFS, devuelve dos diccionarios, uno con los padres de los vértices y otro con el orden '''
    visitados = set()
    visitados.add(origen)
    orden = {}
    padre = {}
    orden[origen] = 0
    padre[origen] = None
    q = deque()
    q.appendleft(origen)
    while(q):
        v = q.pop()
        if v == destino: break
        for w in grafo.adyacentes(v):
            if w in visitados: continue
            padre[w] = v
            orden[w] = orden[v] + 1
            visitados.add(w)
            q.appendleft(w)
    return padre, orden

# --------------------------------------------------------------------- #
#                            CAMINOS MINIMOS                            #
# --------------------------------------------------------------------- #

def camino_minimo_dijkstra(grafo, origen):
    '''Algoritmo de dijkstra para encontrar los caminos minimos de un vertice de origen a todos los demas
    Utiliza un heap a los que se le encolan tuplas cuyos primeros elementos son la prioridad en el heap'''
    distancia = {}
    padre = {}
    for v in grafo:
        distancia[v] = float('inf')
    distancia[origen] = 0
    padre[origen] = None
    heap = []
    heapq.heappush(heap, (distancia[origen], origen))
    while (heap):
        v = heapq.heappop(heap)[1]
        for w in grafo.adyacentes(v):
            if distancia[v] + grafo.peso(v, w) < distancia[w]:
                distancia[w] = distancia[v] + grafo.peso(v, w)
                padre[w] = v
                heapq.heappush(heap, (distancia[w], w))
    return padre, distancia



def camino_minimo_bellman_ford(grafo, origen):
    distancia = {}
    padre = {}
    for v in grafo:
        distancia[v] = float('inf')
    distancia[origen] = 0
    padre[origen] = None
    aristas = grafo.obtener_aristas()
    print(ROJO + f"Aristas: {aristas}" + BLANCO)
    for i in range((len(grafo))):
        for v, w, peso in aristas:
            if distancia[v] + peso < distancia[w]:
                padre[w] = v
                distancia[w] = distancia[v] + peso

    for v,w, peso in aristas:
        if distancia[v] + peso < distancia[w]:
            return None

    return padre, distancia
    

# --------------------------------------------------------------------- #
#                 ORDEN TOPOLÓGICO CON DFS Y BFS                        #
# --------------------------------------------------------------------- #

def hay_ciclo_de_dos(grafo, v, w):
    ''' Devuelve True si hay un ciclo de dos vértices en el grafo, False en caso contrario '''
    return grafo.estan_unidos(v, w) and grafo.estan_unidos(w, v)

def es_subconjunto_bipartito(grafo, subconjunto):
    ''' Devuelve True si un subconjunto perteneciente al grafo es bipartito, False en caso contrario '''
    if len(subconjunto) == 0: return True
    if len(subconjunto) == 2 and hay_ciclo_de_dos(grafo, subconjunto[0], subconjunto[1]):
        return False
        
    color = {}
    for v in subconjunto:
        color[v] = None

    q = deque()
    origen = random.choice(subconjunto)
    q.appendleft(origen)
    color[origen] = "verde"

    while (q):
        v = q.pop()
        for w in subconjunto:
            if not grafo.estan_unidos(v, w): continue
            if color[v] == color[w]:
                return False
            if color[w] == None:
                color[w] = "rojo" if color[v] == "verde" else "verde"
            q.appendleft(w)
        
    return True

def orden_topologico_rec(grafo, v, visitados, lista_orden, subconjunto):
    visitados.add(v)
    for w in subconjunto:
        if w in visitados or not grafo.estan_unidos(v, w): continue
        if v in grafo.adyacentes(w): return
        orden_topologico_rec(grafo, w, visitados, lista_orden, subconjunto)
    lista_orden.append(v)


def orden_topologico_dfs(grafo, subconjunto):
    ''' Recibe un grafo y un subcojunto, y devuelve el orden topológico los elementos del subconjunto
        que pertenezcan al grafo '''
    visitados = set()
    lista_res = []
    for v in subconjunto:   
        if v not in visitados and v in grafo: 
            orden_topologico_rec(grafo, v, visitados, lista_res, subconjunto)
    lista_res.reverse()
    return lista_res

# prueba 75k: lectura Hockey sobre hielo,Roma,Japón,árbol,Guerra,Dios,universo,Himalaya,otoño

# ---------------------------------------------------------------------------- #
#                       COMPONENTES FUERTEMENTE CONEXAS                        #
# ---------------------------------------------------------------------------- #


# Algoritmo de Tarjan

def _cfc(grafo, v, visitados, pila, apilados, orden, mas_bajo, cfcs, indice):
    visitados.add(v)
    pila.append(v)
    apilados.add(v)
    mas_bajo[v] = orden[v]
    for w in grafo.adyacentes(v):
        if w not in visitados:
            orden[w] = indice + 1
            _cfc(grafo, w, visitados, pila, apilados, orden, mas_bajo, cfcs, indice + 1)
            mas_bajo[v] = min(mas_bajo[v], mas_bajo[w])
        elif w in apilados:
            mas_bajo[v] = min(mas_bajo[v], orden[w])
    if mas_bajo[v] == orden[v]:
        nueva_cfc = set()
        while (True):
            w = pila.pop()
            apilados.remove(w)
            nueva_cfc.add(w)
            if w == v: break
            
        cfcs.append(nueva_cfc)

def cfc(grafo, articulo):
    ''' Devuelve una lista con sets, donde cada set es una CFC del grafo '''
    cfcs = []
    visitados = set()
    pila = deque()
    apilados = set()
    orden = {}
    mas_bajo = {}
    for v in grafo:
        orden[v] = 0
        mas_bajo[v] = 0
    _cfc(grafo, articulo, visitados, pila, apilados, orden, mas_bajo, cfcs, 0)
    return cfcs


# ---------------------------------------------------------------------------- #
#                                  PAGERANK                                    #
# ---------------------------------------------------------------------------- #


def vertices_entrantes(grafo, vertice):
    ''' Devuelve un set con los vértices entrantes al vértice pasado por parámetro'''
    resultado = set()
    for v in grafo:
        if grafo.estan_unidos(v, vertice):
            resultado.add(v)
    return resultado


def cargar_diccionarios_pagerank(grafo):
    ''' Función auxiliar para cargar los diccionarios que se utilizan en PageRank '''
    pr = {}
    entrantes = {}
    len_adyacentes = {}
    for v in grafo:
        for w in grafo.adyacentes(v):
            if v not in len_adyacentes:
                len_adyacentes[v] = 0
            len_adyacentes[v] += 1

            if w not in entrantes:
                entrantes[w] = set()
            entrantes[w].add(v)

        pr[v] = 1
    return pr, entrantes, len_adyacentes

def page_rank(grafo):
    ''' Algoritmo de PageRank '''
    
    pr, entrantes, len_adyacentes = cargar_diccionarios_pagerank(grafo)

    contador = 0 
    while (contador != K):
        anterior = pr
        for v in grafo:
            suma = 0 
            if v in entrantes:
                for w in entrantes[v]:
                    suma += pr[w] / len_adyacentes[w]
            res = (1 - D) + (D * suma)
            pr[v] = res
        if anterior == pr:
            contador += 1
    return pr


# ---------------------------------------------------------------------------- #
#                                   DIAMETRO                                   #
# ---------------------------------------------------------------------------- #

def diametro(grafo):
    ''' Función que calcula el máximo camino mínimo del grafo recibido
        Devuelve un diccionario de padres, los vértices de origen y destino y el valor del diámetro'''
    res_diametro = 0
    res_camino = {}
    desde, hasta = (None, None)
    for v in grafo:
        padre, distancia = bfs(grafo, v, None)
        for w in distancia:
            if distancia[w] > res_diametro:
                res_diametro = distancia[w]
                res_camino = padre
                desde, hasta = v, w
    return res_camino, res_diametro, desde, hasta
    