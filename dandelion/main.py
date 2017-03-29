"""Defines the Dandelion class"""
import networkx as nx;

class Dandelion:
    """The Dandelion code"""

    def __init__(self, N, k, code = None, kTree = None):
        """Initializes the code."""

        self.N = N;
        self.k = k;
        if code is not None:
            self.code = code;
        if kTree is not None:
            self.kTree = kTree;

    @property
    def code(self):
        return self._code;

    @code.setter
    def code(self, value):
        self.validateCode(value);
        self._code = value;

    @property
    def kTree(self):
        return self._kTree;

    @kTree.setter
    def kTree(self, value):
        self.validateKTree(value);
        self._kTree = value;

    def validateCode(self, code):
        """Check if the code is well formed.

        Raises AssertionError if not.
        """

        #Check types
        assert isinstance(code, list);
        for t in code:
            assert isinstance(t, tuple);

        #Assert number of elements according to N and k
        assert len(code) == self.N - self.k - 2

        return True;

    def validateKTree(self, kTree):
        """Check if the kTree is correct.

        DOES NOT validates the kTree structure, instead does minimum validation
        to check if it an instance of networkx's Graph.
        """

        assert isinstance(kTree, nx.Graph)
        return True;

    def codeKTree(self):
        """Code a kTree into a Dandelion code.

        Needs to have the kTree attribute set.
        Fills the code attribute (rewrites it if there was any).
        """
        if self.kTree is None:
            raise Error("Need to specify a k-Tree first");

        #Turn the kTree into a Renyi kTree:
        Q, renyiKTree = _relabelKTree(self.kTree);

        #Obtain the characteristic tree from the Renyi kTree:
        ## Create Node List
        T = _pruneRk(renyiKTree);
        ## Create Edge List
        _addEdges(T);

        #Obtain the Dandelion Code from the characteristic tree:
        #TODO

    def _addEdges(self, T):
        #TODO
        return True;

    def _pruneRk(self, Rk):
        """Creates a new characteristic tree T from a Renyi kTree.

        Returns a new Graph, with just the nodes for T but no edges. All nodes
        except for the root in the Renyi kTree are marked as checked in the
        process.

        Parameters:
            Rk: nx.Graph
                The Renyi kTree

        Returns:
            T: nx.Graph
                The characteristic tree with only the node list.

        """
        T = nx.Graph();

        nx.set_node_attributes(Rk, 'checked', False);
        adj = Rk.adjacency_list();
        deg = Rk.degree();

        def remove(node):
            T.add_node(node);
            Rk.node[node]['checked'] = True;
            for y in adj[node-1]:
                if not Rk.node[y]['checked']:
                    deg[y] -= 1;

        for v, _ in enumerate(range(self.N - self.k), 1):
            if deg[v] == self.k:
                remove(v);
                for u in adj[v-1]:
                    if u < v and not Rk.node[u]['checked'] and deg[u] == self.k:
                        remove(u);
        return T;

    def _relabelKTree(self, kTree):
        """Transforms the k-Tree into a Renyi k-Tree.

        Creates a new graph from the input kTree.

        Parameters
        kTree : networkx.Graph
            The kTree

        Returns
        Q : list
            A sorted list of nodes with degree = k
        renyiKTree : networkx Graph
            The relabeled kTree.
        """

        renyiKTree = nx.Graph();
        renyiKTree.add_edges_from(kTree.edges())

        #l_m is the maximum node of degree k
        l_m = max([k for k, v in kTree.degree().items() if v == self.k]);
        #Q are the nodes adjacent to l_m
        Q = sorted(list(kTree[l_m].keys()));

        #Step 1:
        R = [self.N - self.k + i + 1 for i in range(self.k)] #New root
        mapping = {k: v for k, v in zip(Q, R)}
        #Step 2 is not needed
        #Step 3:
        loopClosers = [i for i in R if i not in Q];
        for lc in loopClosers:
            newLabel = lc;
            while newLabel in mapping.values():
                #Find dict keys by value
                newLabel = list(mapping.keys())[list(mapping.values()).index(newLabel)]
            mapping.update({lc: newLabel});

        #Actual relabel
        nx.relabel_nodes(renyiKTree, mapping);

        return Q, renyiKTree;

def main():
    """Parses command line arguments"""
    return None

if __name__ == "__main__":
    main()
