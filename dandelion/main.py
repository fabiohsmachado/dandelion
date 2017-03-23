"""Defines the Dandelion class"""
import networkx as nx;

class Dandelion:
    """The Dandelion code"""

    def __init__(self, N, k, code=None, kTree=None):
        """Initializes the code."""

        self.N = N;
        self.k = k;
        self._code = None;
        self._kTree = None;
        if code is not None:
            self.code = code;
        if kTree is not None:
            self.kTree = kTree;

    # The code itself. Each i-th element of the array is a tuple containing the
    # parent of the i-th node and its edge label in the characteristic tree.
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
        Fills the code attribute and rewrites it if there was any.
        """
        if self.kTree is None:
            raise Error("Need to specify a k-Tree first");

        renyiKTree = _relabelKTree(self.kTree);

        return mapping;

    def _relabelKTree(self, kTree):
        """Transforms the k-Tree into a Renyi k-Tree.

        Creates a new graph from the input kTree.

        Parameters
        kTree : networkx.Graph
            The kTree

        Returns
        renyiKTree : networkx Graph
            The relabeled kTree.
        """

        renyiKTree = nx.Graph();
        renyiKTree.add_edges_from(kTree.edges())

        #l_m is the maximum node of degree k
        l_m = max([k for k, v in kTree.degree().items() if v == self.k]);
        #Q are the nodes adjacent to l_m
        Q = sorted(list(kTree[l_m].keys()));


        ##Step 1:
        R = [self.N - self.k + i + 1 for i in range(self.k)] #New root
        mapping = {k: v for k, v in zip(Q, R)}
        ##Step 2 is not needed
        ##Step 3:
        loopClosers = [i for i in R if i not in Q];
        for lc in loopClosers:
            try:
                newLabel = lc;
                while True:
                    #Find dict keys by value
                    newLabel = list(mapping.keys())[list(mapping.values()).index(newLabel)]
            except ValueError:
                pass;
            mapping.update({lc: newLabel});

        ##Actual relabel
        nx.relabel_nodes(renyiKTree, mapping);

        return renyiKTree;

def main():
    """Parses command line arguments"""
    return None

if __name__ == "__main__":
    main()
