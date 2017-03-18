import pytest
from ..main import Dandelion

class TestDandelion():
    """Tests for the Dandelion code"""

    N, k = 11, 3;
    good_code = [(0, -1), (2, 1), (8, 3), (8, 2), (1, 3), (5, 3)];
    bad_code = [(0, -1), (0, 2), 4, [1, 3]]

    def test_dandelion_constructs_good_code(self):
        assert isinstance(Dandelion(11, 3, self.good_code), Dandelion);

    def test_dandelion_validates_bad_code_structure(self):
        with pytest.raises(AssertionError):
            Dandelion(11, 3, self.bad_code);

    def test_dandelion_validates_bad_code_length(self):
        DCode = Dandelion(11, 3);

        codeString = [(0, -1), (0, 2)]
        with pytest.raises(AssertionError):
            DCode.validateCode(codeString);

    def test_assigning_new_code_validates_it(self):
        DCode = Dandelion(11, 3);
        with pytest.raises(AssertionError):
            DCode.code = self.bad_code;

    def test_requesting_code_returns_it(self):
        DCode = Dandelion(11, 3);
        DCode.code = self.good_code;
        assert DCode.code == self.good_code;

    def test_request_empty_code_returns_none(self):
        DCode = Dandelion(11, 3);
        assert DCode.code == None;
