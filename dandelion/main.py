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

def main():
    """Parses command line arguments"""
    return None

if __name__ == "__main__":
    main()
