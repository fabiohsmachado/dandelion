import pytest

import networkx as nx
import numpy as np

from ..main import Dandelion

class TestDandelion():
    """Tests for the Dandelion code"""

    N = 11
    k = 3;
    good_code = [(0, -1), (2, 1), (8, 3), (8, 2), (1, 3), (5, 3)];
    bad_code = [(0, -1), (0, 2), 4, [1, 3]];

    #Example Fig 1
    kTree = nx.Graph();
    kTree.add_edges_from([(1,2),(1,8),(1,5),(1,7),
                          (2,5),(2,6),(2,8),(2,3),(2,11),(2,9),(2,10),
                          (3,8),(3,5),(3,9),(3,4),(3,10),(3,11),
                          (4,9),(4,11),
                          (5,7),(5,8),
                          (6,9),(6,8),
                          (7,8),
                          (8,9),
                          (9,10),(9,11)])

    renyiKTree = nx.Graph();
    renyiKTree.add_edges_from(kTree.edges());
    nx.relabel_nodes(renyiKTree, {2:9, 3:10, 9:11, 10:3, 11:2})

    #Example of Fig. 2
    Rk = nx.Graph();
    Rk.add_edges_from([(1,9),(1,5),(1,8),(1,7),
                       (2,10),(2,11),(2,9),(2,4),
                       (3,9),(3,11),(3,10),
                       (4,11),(4,10),
                       (5,9),(5,8),(5,10),(5,7),
                       (6,9),(6,8),(6,11),
                       (7,8),
                       (8,9),(8,11),(8,10),
                       (9,11),(9,10),
                       (10,11)])

    T = nx.Graph();
    T.add_nodes_from([1, 2, 3, 4, 5, 6, 7, 8])
    T.add_edges_from([#(0, 3, {'label':-1}), (0, 8, {'label':-1}), (0, 2, {'label':-1}),
                          (8, 5, {'label':3}), (8, 6, {'label':2}),
                          (2, 4, {'label':1}),
                          (5, 1, {'label':3}),
                          (1, 7, {'label':3})]);


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

    def test_dandelion_tranforms_kTree_into_renyiKTree(self):
        DCode = Dandelion(11, 3, kTree = self.kTree);
        Q, RTree = DCode._relabelKTree(self.kTree);
        assert RTree.edges() == self.renyiKTree.edges() and Q == [2, 3, 9];

    def test_dandelion_creates_node_list_for_the_characteristc_tree(self):
        #Asserts T has the same node list
        DCode = Dandelion(11, 3);
        T = DCode._pruneRk(self.Rk);
        assert T.nodes() == self.T.nodes();

        #Asserts all nodes in Rk, except for the Root were checked
        checkedAttr =  {i: True for i in T.nodes()}
        checkedAttr.update({9: False, 10: False, 11: False});
        assert nx.get_node_attributes(self.Rk, 'checked') == checkedAttr;
