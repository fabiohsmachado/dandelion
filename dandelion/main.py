"""Defines the Dandelion class"""

class Dandelion:
    """The Dandelion code"""

    def __init__(self, initialCode=None):
        """Initializes the code. An already existing code can be passed too."""

        self._code = None;
        if initialCode is not None:
            self.code = initialCode;
            self.N = len(self.code) + 2;

    # The code itself. Each i-th element of the array is a tuple containing the
    # parent of the i-th node and its edge label in the characteristic tree.
    @property
    def code(self):
        return self._code;

    @code.setter
    def code(self, value):
        self.validateCode(value);
        self._code = value;

    #The number of variables in the k-Tree
    N = None;

    def validateCode(self, code):
        """Check if the code is well formed"""

        #Assert types
        assert isinstance(code, list);
        for t in code:
            assert isinstance(t, tuple);

        #If N exists assert number of elements according to N
        if self.N is not None:
            assert len(code) == self.N - 2

        return True;

def main():
    """Parses command line arguments"""
    return None

if __name__ == "__main__":
    main()
