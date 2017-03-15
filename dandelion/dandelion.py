"""Defines the Dandelion class"""

class Dandelion:
    """The Dandelion code"""

    # The code itself. Each i-th element of the array is a set containing the
    # parent of the i-th node and its edge label in the characteristic tree.
    code = []

    def __init__(self, code=None):
        """Initializes the code. An already existing code can be passed too."""
        if code is not None:
            self.code = code;

def main():
    """Parses command line arguments"""
    return None

if __name__ == "__main__":
    main()
