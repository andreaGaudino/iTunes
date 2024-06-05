import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.graph = nx.Graph()
        self.idMap = {}

    def getSetAlbum(self, a1, dTOT):
        self.bestSet = None
        self.bestScore = 0
        connessa = nx.node_connected_component(self.graph, a1)
        parziale = set([a1])
        connessa.remove(a1)

        self.ricorsione(parziale, connessa, dTOT)
        return self.bestSet, self.durataTot(self.bestSet)


    def ricorsione(self, parziale, connessa, dTOT):
        if self.durataTot(parziale) > dTOT:
            return

        if len(parziale) > self.bestScore:
            self.bestSet = copy.deepcopy(parziale)
            self.bestScore = len(parziale)


        for c in connessa:
            if c not in parziale:
                parziale.add(c)
                rimanenti = copy.deepcopy(connessa)
                rimanenti.remove(c)
                self.ricorsione(parziale, rimanenti, dTOT)
                parziale.remove(c)




    def durataTot(self, listOfNodes):
        dtot = 0
        for n in listOfNodes:
            dtot += toMinutes(n.totD)
        return dtot


    def buildGraph(self, d):
        self.graph.clear()
        self.graph.add_nodes_from(DAO.getAlbums(toMilliseconds(d)))
        self.idMap = {}
        self.idMap = {a.AlbumId : a for a in list(self.graph.nodes)}
        edges = DAO.getEdges(self.idMap)

        self.graph.add_edges_from(edges)

    def getConnessaDetails(self, v0):
        conn = nx.node_connected_component(self.graph, v0)
        durataTot = 0
        for album in conn:
            durataTot += toMinutes(album.totD)

        return len(conn), durataTot

    def getGraphDetails(self):
        return len(self.graph.nodes), len(self.graph.edges)

    def getNodes(self):
        return list(self.graph.nodes)
    def getNodeI(self, i):
        return self.idMap[i]




def toMinutes (d):
    return d/1000/60

def toMilliseconds(d):
    return d*60*1000