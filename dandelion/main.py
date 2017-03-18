"""Defines the Dandelion class"""

class Dandelion:
    """The Dandelion code"""

    def __init__(self, N, k, initialCode=None):
        """Initializes the code."""

        self.N = N;
        self.k = k;
        self._code = None;
        if initialCode is not None:
            self.code = initialCode;

    # The code itself. Each i-th element of the array is a tuple containing the
    # parent of the i-th node and its edge label in the characteristic tree.
    @property
    def code(self):
        return self._code;

    @code.setter
    def code(self, value):
        self.validateCode(value);
        self._code = value;

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

def main():
    """Parses command line arguments"""
    return None

if __name__ == "__main__":
    main()
