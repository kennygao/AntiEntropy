class Node:
    def __init__(self, adjacent_nodes=[], data={}):
        # data length must be power of 2
        self.adjacent_nodes = adjacent_nodes
        self.data = data
        self.merkle = self.tomerkle()
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
    def merklediff(self, other, level=0, position=0):
        if level >= len(self.merkle):
            return position, other.merkle[-1][position]
        for i, x in enumerate(self.merkle[level][2 * position:2 * position + 2]):
            # print('{} {} {}'.format(self.merkle[level][i], other.merkle[level][i], i))
            # print(self.merkle[level][2 * position:2 * position + 2])
            if not self.merkle[level][2 * position + i] == other.merkle[level][2 * position + i]:
                return self.merklediff(other, level + 1, 2 * position + i)
        return None

##########

import random

testdata = map(str, random.sample(range(1000), 16))
node = Node(data = testdata)
other = Node(data = [str(int(testdata[0]) + 1)] + testdata[1:])
third = Node(data = testdata[0:-1] + [str(int(testdata[-1]) + 1)])

print('--- Node 1:')
print(node)
print('--- Node 1 Merkle Tree:')
for x in node.tomerkle():
    print(x)

print('')

print('--- Node 2:')
print(other)
print('--- Node 2 Merkle Tree:')
for x in other.tomerkle():
    print(x)

print('')

print('--- Node 3:')
print(third)
print('--- Node 3 Merkle Tree:')
for x in third.tomerkle():
    print(x)

print('')

print('Node 1 and Node 2 differ at {}'.format(node.merklediff(other)))
print('Node 1 and Node 3 differ at {}'.format(node.merklediff(third)))

# for x in range(9):
#     nodes.append(Node(nodes[x], random.sample(range(1000), 10)))

# print(nodes)

