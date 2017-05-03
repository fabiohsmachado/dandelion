"""Defines the Dandelion class"""
import networkx as nx;

class Dandelion:
    """The Dandelion code"""

    def __init__(self, N, k, code = None, kTree = None):
        """Initializes the code."""

        self.N = N;
        self.k = k;
        self._code = None;
        self._kTree = None;
        if code is not None:
            self.code = code;
        if kTree is not None:
            self.kTree = kTree;

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

        Raises:
            AssertionError: If it is not a valid code.
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

        Raises:
            AssertionError: If it is not a valid kTree
        """

        assert isinstance(kTree, nx.Graph)
        return True;

    def codeKTree(self):
        """Code a kTree into a Dandelion code.

        Needs to have the kTree attribute set.
        Fills the code field of this object (rewrites it if there was any).

        Raises:
            Error: If the kTree field of the Dandelion object is not filled.
        """
        if self.kTree is None:
            raise Error("Need to specify a k-Tree first");

        #Turn the kTree into a Renyi kTree:
        self.Q, self.Rk = self._relabelKTree(self.kTree);

        #Obtain the characteristic tree T from the Renyi kTree:
        self.T = self._pruneRk();

        #Obtain the Dandelion Code from the characteristic tree:
        ##Setup parameters
        r = 0;

        nodesInT = [i for i in self.T][1:];
        q_bar = min([n for n in nodesInT if n not in self.Q]);
        x = self.Rk.node[q_bar]['old_label'];

        ##Generate the code
        self.code = self._generalizedCode(self.T, r, x);

        return self.Q, self.code;

    def _generalizedCode(self, T, r, x):
        """Generates a dandelion code from a given characteristic tree.

        The input tree is modified so it has the cicles that results from
        generating the code.

        Parameters:
            T: nx.DiGraph
                The input characteristic tree.

            r: Graph node
                The root node of the tree (usually 0)

            x: Graph node
                The minimal node not belonging to the original root

        Returns:
            code:
                List of tuples The generalized dandelion code for the
                given characteristic tree
        """
        def swap(source, target):
            """Provides a method for swaping nodes in a graph.

            This function removes the original edge of each node with its
            parent and add a new edge with one node and the other node's
            parent. It preserves the original label.
            """
            labels = nx.get_edge_attributes(T, 'label');
            parent_source = T.successors(source)[0];
            label_source = labels[(source, parent_source)];

            parent_target = T.successors(target)[0];
            label_target = labels[(target, parent_target)];

            T.remove_edge(source, parent_source);
            T.remove_edge(target, parent_target);
            T.add_edge(source, parent_target, label = label_target);
            T.add_edge(target, parent_source, label = label_source);

        path = nx.shortest_path(T, x, r)[1:-1];
        while(len(path) > 0):
            w = max(path);
            swap(x, w);
            path = nx.shortest_path(T, x, r)[1:-1];

        nodes = sorted([v for v in T.nodes() if v not in [x, r]]);
        labels = nx.get_edge_attributes(T, 'label');
        code = [];
        for v in nodes:
            p_v = T.successors(v)[0]
            code.append((p_v, labels[(v, p_v)]));

        return code[1:];

    def _pruneRk(self):
        """Wrapper function for generating the characteristic tree.

        Creates a new tree, and separatedly populates its nodes and edge list.

        Returns
            T: nx.DiGraph
                The new characteristic tree
        """
        T = nx.DiGraph();
        pruneOrder = self._addNodes(self.Rk, T);
        self._addEdges(T, pruneOrder);
        return T;

    def _addEdges(self, T, pruneOrder):
        """Updates the characteristic three with the edge list according to the pruning
        order.

        The edge list are filled using the reversed pruning order and the
        adjacent clique store in each node.

        Parameters:
            T: nx.DiGraph
                The characteristic tree with a filled node list

            pruneOrder: list
                The prune order defined when the nodes were added

        """
        #Initialize control variables
        R = [self.N - self.k + i + 1 for i in range(self.k)]; #Root of the Renyi kTree
        level = [0 for i in range(self.N)]; #All nodes levels start at 0

        for v in reversed(pruneOrder):
            Kv = T.node[v]['Kv'];

            if Kv == R:
                T.add_edge(v, 0, label = -1);
                level[v-1] = 1;

            else:
                #Choose w in Kv such that level(w) is maximum
                levelsInKv = [level[x-1] for x in Kv];
                indexOfW = levelsInKv.index(max(levelsInKv));
                w = Kv[indexOfW];

                #The edge label is the index only element in Kw that does not
                #belong to Kv
                Kw = T.node[w]['Kv'];
                edge_label = [i for i, v in enumerate(Kw, 1) if v not in Kv][0];

                T.add_edge(v, w, label = edge_label);
                level[v-1] = level[w] + 1;

    def _addNodes(self, Rk, T):
        """Updates the characteristic tree T from a given Renyi kTree.

        Updates T with the list of nodes and their adjacent cliques after the
        pruning process. The adjacent clique is stored in a 'Kv' attribute of
        each node. The pruning order is returned from the function.

        All nodes except for the root in the Renyi kTree are marked as checked
        in the process.

        Parameters:
            Rk: nx.Graph
                The Renyi kTree

            T: nx.Graph
                The Characteristic tree to be filled with nodes

        Returns:
            pruneOrder: list
                list The list of node in the order they were pruned
        """
        def remove(node):
            #Record the prune order
            pruneOrder.append(node);

            #Get the adjacent clique and add node to the graph
            AdjacentClique = sorted([x for x in Rk[node] if not Rk.node[x]['checked']]);
            T.add_node(node, Kv = AdjacentClique);

            #Mark as removed and update degree list
            Rk.node[node]['checked'] = True;
            for y in adj[node-1]:
                if not Rk.node[y]['checked']:
                    deg[y] -= 1;


        #Initialize parameters
        nx.set_node_attributes(Rk, 'checked', False);
        T.add_node(0);

        #initialize control variables
        pruneOrder = [];
        adj = Rk.adjacency_list();
        deg = Rk.degree();

        for v, _ in enumerate(range(self.N - self.k), 1):
            if deg[v] == self.k:
                remove(v);
                for u in adj[v-1]:
                    if u < v and not Rk.node[u]['checked'] and deg[u] == self.k:
                        remove(u);

        return pruneOrder;

    def _relabelKTree(self, kTree):
        """Transforms the k-Tree into a Renyi k-Tree.

        Creates a new relabeled tree.
        Old labels are stored as a properties of the nodes to be able to reverse the relabel.

        PARAMETERS
        KTREE : networkx.Graph
            The kTree

        Returns
        Q : list
            A sorted list of nodes with degree = k
        renyiKTree : networkx Graph
            The relabeled kTree.
        """
        renyiKTree = nx.Graph();
        renyiKTree.add_edges_from(kTree.edges())

        #l_m is the maximum node of degree k
        l_m = max([k for k, v in kTree.degree().items() if v == self.k]);

        #Q are the nodes adjacent to l_m
        Q = sorted(list(kTree[l_m].keys()));

        #Those are the algorithm steps as decribed in the paper
        ##Step 1: Define the new root and relabel node in Q for nodes in R
        R = [self.N - self.k + i + 1 for i in range(self.k)] #New root
        mapping = {k: v for k, v in zip(Q, R)}

        ##Step 2: Nothing needs to be done, just not remap those nodes

        ##Step 3: Close permutation cycles
        loopClosers = [i for i in R if i not in Q];
        for lc in loopClosers:
            newLabel = lc;
            while newLabel in mapping.values():
                #Find dict keys by value
                newLabel = list(mapping.keys())[list(mapping.values()).index(newLabel)]
            mapping.update({lc: newLabel});

        #Actual relabel
        nx.set_node_attributes(renyiKTree, 'old_label', {n: n for n in
                                                         renyiKTree.nodes()}) #Save old node labels
        return Q, nx.relabel_nodes(renyiKTree, mapping); #Update node labels
