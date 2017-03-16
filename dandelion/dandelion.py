"""Defines the Dandelion class"""

class Dandelion:
    """The Dandelion code"""

    # The code itself. Each i-th element of the array is a set containing the
    # parent of the i-th node and its edge label in the characteristic tree.
    code = [];

    #The number of variables in the k-Tree
    N = None;

    def validateCode(code):
        """Check if the code is well formed"""

        #Assert types
        assert isinstance(code, list);
        for t in code:
            assert isinstance(t, tuple);

        #Assert number of elements according to N
        assert len(code) == self.N - 2

        return True;

    def __init__(self, code=None):
        """Initializes the code. An already existing code can be passed too."""
        if code is not None:
            try:
                self.validateCode(code);
            except AssertionError:
                return "Invalid code";

            self.code = code;
            self.N = len(code) + 2;

def main():
    """Parses command line arguments"""
    return None

if __name__ == "__main__":
    main()
