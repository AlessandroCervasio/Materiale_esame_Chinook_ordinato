import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph=None
        self._MapArtistId={}
        artisti=DAO.getAllArtists()
        for a in artisti:
            self._MapArtistId[a.ArtistId]=a

        self._longestPath=[]

        self._camminoPesoASC=[]

    # all musical genres - tutti i generi musicali
    def getAllGenres(self):
        return DAO.getAllGenres()
    # all artists - tutti gli artisti
    def getAllArtists(self):
        return DAO.getAllArtists()
    # all artists from a given genre - tutti gli artisti dato un genere
    def getAllArtistsGenre(self, genreId):
        return DAO.getArtistGenre(genreId)

    # nodi: artisti che possiedono almeno un brano del genere selezionato
    # archi: artisti per cui esiste almeno un cliente che ha acquistato brani di entrambi gli artisti
    # peso: somma delle popolarità (brani acquistati dell'artista appartenenti al genere scelto)
    def buildGraph(self, genreId):
        self._graph= nx.DiGraph()
        nodi= DAO.getArtistGenre(genreId)
        self._graph.add_nodes_from(nodi)
        archi = DAO.getCoppieArtistGenre(genreId)
        for a in archi:
            u= self._MapArtistId[a[0]]
            v= self._MapArtistId[a[1]]

            pop_u= DAO.getPopolaritaArtistGenre(a[0], genreId)
            pop_v = DAO.getPopolaritaArtistGenre(a[1], genreId)
            weight= pop_u+pop_v
            if u in self._graph.nodes and v in self._graph.nodes:
                if pop_u > pop_v:
                    self._graph.add_edge(u, v, weight=weight)
                elif pop_v > pop_u:
                    self._graph.add_edge(v, u, weight=weight)
                else:
                    self._graph.add_edge(u, v, weight=weight)
                    self._graph.add_edge(v, u, weight=weight)


    # artista più influente / nodi in ordine di influenza
    def getArtistaPiuInfluente(self):
        lista_tuple_artisti_influenza=[]
        for artista in self._graph.nodes:
            peso_out = self._graph.out_degree( weight="weight")[artista]
            peso_in = self._graph.in_degree( weight="weight")[artista]

            influenza= peso_out - peso_in
            lista_tuple_artisti_influenza.append((artista, influenza))

        artisti_ordinati_influenza= sorted(lista_tuple_artisti_influenza, key=lambda x: x[1], reverse= True)
        return artisti_ordinati_influenza[0]


    # archi di peso maggiore
    def getArchiPesoMaggiore(self):
        archi_ord= list(sorted(self._graph.edges (data=True), key=lambda x: x[2]["weight"], reverse = True))
        return archi_ord[:5]


    # graph details
    def getGraphDetails (self):
        n_nodi= len(self._graph.nodes)
        n_archi = len(self._graph.edges)
        return n_nodi, n_archi

    # percorso più lungo con ricorsiva
    def getLongestPath(self, source):
        parziale=[source]
        self.ricorsivaLongestPath(parziale)
        return self._longestPath

    def ricorsivaLongestPath(self, parziale):
        if len(parziale)>len(self._longestPath):
            self._longestPath=copy.deepcopy(parziale)

        successivi= self._graph.successors(parziale[-1])
        for s in successivi:
            if s not in parziale:
                parziale.append(s)
                self.ricorsivaLongestPath(parziale)
                parziale.pop()

    # cammmino di lunghezza massima con peso degli archi crescente
    def getCamminoPesoASC(self, source):
        parziale = [source]
        self.ricorsivaCamminoPesoASC(parziale)
        return self._camminoPesoASC

    def ricorsivaCamminoPesoASC (self, parziale):
        if len(parziale)> len(self._camminoPesoASC):
            self._camminoPesoASC=copy.deepcopy(parziale)
        successori= self._graph.successors(parziale[-1])
        for s in successori:
            if s not in parziale:
                if len(parziale)<=1:
                    peso_prec=0
                else:
                    peso_prec=self._graph[parziale[-2]][parziale[-1]]["weight"]

                if peso_prec< self._graph[parziale[-1]][s]["weight"]:
                    parziale.append(s)
                    self.ricorsivaCamminoPesoASC(parziale)
                    parziale.pop()






