import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.graph = nx.Graph()
        self.idMap = {}

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
def toMinutes (d):
    return d/1000/60

def toMilliseconds(d):
    return d*60*1000