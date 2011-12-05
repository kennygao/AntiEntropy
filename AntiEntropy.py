class Node:
    def __init__(self, adjacent_nodes=[], data={}):
        # data length must be power of 2
        self.adjacent_nodes = adjacent_nodes
        self.data = data
    def __str__(self):
        # return str((self.adjacent_nodes, self.data))
        return str(self.data)
    def __repr__(self):
        return self.__str__()
    def merklehash(self, s):
        return str(s.__hash__())
    def tomerkle(self):
        tree = [map(self.merklehash, self.data)]
        i = len(self.data)
        while i > 1:
            i /= 2
            tmp = []
            for x in range(i):
                tmp.append(self.merklehash(tree[0][2 * x] + tree[0][2 * x + 1]))
            tree.insert(0, tmp)
        return tree

import random

testdata = map(str, random.sample(range(1000), 16))
node = Node(data = testdata)
other = Node(data = [testdata[0] + "."] + testdata[1:])

print(node)
for x in node.tomerkle():
    print(x)

print(other)
for x in other.tomerkle():
    print(x)

# for x in range(9):
#     nodes.append(Node(nodes[x], random.sample(range(1000), 10)))

# print(nodes)

