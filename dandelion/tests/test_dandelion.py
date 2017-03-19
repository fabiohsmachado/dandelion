import pytest

import networkx as nx
import numpy as np
from ..main import Dandelion

class TestDandelion():
    """Tests for the Dandelion code"""

    N, k = 11, 3;
    good_code = [(0, -1), (2, 1), (8, 3), (8, 2), (1, 3), (5, 3)];
    bad_code = [(0, -1), (0, 2), 4, [1, 3]];

    kTree = nx.Graph();
    kTree.add_nodes_from([i for i in np.arange(N)]);
    kTree.add_edges_from([(1,2),(1,8),(1,5),(1,7),
                          (2,5),(2,6),(2,8),(2,3),(2,11),(2,9),(2,10),
                          (3,8),(3,5),(3,9),(3,4),(3,10),(3,11),
                          (4,9),(4,11),
                          (5,7),(5,8),
                          (6,9),(6,8),
                          (7,8),
                          (8,9),
                          (9,10),(9,11)])

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

    def test_dandelion_constructs_from_kTree(self):
        DCode = Dandelion(11, 3, kTree=self.kTree);
        assert DCode.kTree == self.kTree;

    def test_dandelion_validates_bad_kTree(self):
        DCode = Dandelion(11, 3);
        with pytest.raises(AssertionError):
            DCode.kTree = [11, 5] #Not an instance of nx.Graph;
