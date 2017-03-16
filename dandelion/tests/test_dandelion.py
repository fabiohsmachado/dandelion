import pytest
from .. import dandelion

class TestDandelion():
    """Tests for the Dandelion code"""

    code = [(0,-1), (0, -1), (2, 1), (8, 3), (8, 2), (1, 3), (5, 3)];

    def test_dandelion_constructor_good_code(self):
        assert isinstance(dandelion.Dandelion(self.code), dandelion.Dandelion)

    def test_dandelion_validates_bad_code_structure(self):
        code = [(0, -1), (0, 2), [1, 3]]
        with pytest.raises(AssertionError):
            dandelion.Dandelion(code)

    def test_dandelion_validates_bad_code_length(self):
        codeString = [(0, -1), (0, 2)]
        code = dandelion.Dandelion()
        code.N = 5;

        with pytest.raises(AssertionError):
            code.validateCode(codeString)
