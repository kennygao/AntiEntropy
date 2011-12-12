class Node:
    def __init__(self, adjacent_nodes=[], data={}):
        # data length must be power of 2
        self.adjacent_nodes = adjacent_nodes
        self.data = data
        self.tomerkle()
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
        self.merkle = tree
        return tree
    def merklediff(self, other, level=0, index=0):
        if level >= len(self.merkle):
            return index, other.merkle[-1][index]
        for i, x in enumerate(self.merkle[level][2 * index:2 * index + 2]):
            if not self.merkle[level][2 * index + i] == other.merkle[level][2 * index + i]:
                return self.merklediff(other, level + 1, 2 * index + i)
        return None
    # poll neighbors; majority wins
    def resolveconflict(self, other, index):
        if self.data[index] == other.data[index]:
            return
        keep = 0
        change = 0
        for adj in self.adjacent_nodes:
            if adj.data[index] == self.data[index]:
                keep += 1
            elif adj.data[index] == other.data[index]:
                change += 1
        # in case of ties, keep
        if change > keep:
            self.data[index] = other.data[index]
        else:
            other.data[index] = self.data[index]
        self.tomerkle()
        other.tomerkle()

##########

import random

testdata = map(str, random.sample(range(1000), 16))
node = Node(data = testdata)
other = Node(data = [str(int(testdata[0]) + 1)] + testdata[1:])
third = Node(data = testdata[0:-1] + [str(int(testdata[-1]) + 1)])
fourth = Node(data = testdata)
node.adjacent_nodes = [other, third, fourth]
other.adjacent_nodes = [node, third, fourth]
third.adjacent_nodes = [node, other, fourth]

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

print('Before repair: Node 1 and Node 2 differ at {}'.format(node.merklediff(other)))
node.resolveconflict(other, node.merklediff(other)[0])
print('After repair: Node 1 and Node 2 differ at {}'.format(node.merklediff(other)))

print('Before repair: Node 1 and Node 3 differ at {}'.format(node.merklediff(third)))
node.resolveconflict(third, node.merklediff(third)[0])
print('After repair: Node 1 and Node 3 differ at {}'.format(node.merklediff(third)))

