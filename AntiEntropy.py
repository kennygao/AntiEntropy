class Replica:
    class Datum:
        def __init__(self, datum, timestamp):
            self.datum = datum
            self.timestamp = timestamp
        def __repr__(self):
            return str((self.datum, self.timestamp))

    class MerkleNode:
        def __init__(self, value, left, right, isleaf=False, level=0, index=0):
            self.value = value
            self.left = left
            self.right = right
            self.isleaf = isleaf
            self.level = level
            self.index = index

    # initialize data and compute initial merkle tree
    def __init__(self, data=[], offset=[0, 0]):
        # assumption (without loss of generality): data length must be power of 2
        self.data = data
        self.offset = offset
        self.computemerkle()
    # hash function used by merkle tree computation
    def merklehash(self, s):
        # do we care if the data match but the timestamps don't?
        return str(s.__hash__())
    # compute and set merkle tree
    def computemerkle(self):
        # children refers to most recently computed level
        children = [self.MerkleNode(self.merklehash(d.datum), None, None, True, 0, i) for i, d in enumerate(self.data)]
        [drawnode(child, self.offset) for child in children]
        l = len(self.data)
        level = 0
        while l > 1:
            l /= 2
            level += 1
            parents = []
            for x in range(l):
                node = self.MerkleNode(self.merklehash(children[2 * x].value + children[2 * x + 1].value),
                                       children[2 * x],
                                       children[2 * x + 1],
                                       False,
                                       level,
                                       x)
                parents.append(node)
                drawnode(node, self.offset)
            children = parents
        # set to root node
        self.merkle = children[0]
    # print merkle tree
    def printmerkle(self):
        level = [self.merkle]
        print(self.merkle.value)

        # holy shit this is so sexy
        while not level[0].isleaf:
            nextlevel = [(n.left, n.right) for n in level]
            level = [child for children in nextlevel for child in children] # flatten list
            print(", ".join([n.value for n in level]))
    def synchronize(self, origin, originnode=None, selfnode=None, index=0):
        if originnode == None:
            originnode = origin.merkle
        if selfnode == None:
            selfnode = self.merkle

        if originnode.value == selfnode.value:
            print('   Hashes match. Returning from subtree.')
            return []
        elif not originnode.isleaf:
            print('   Hashes do not match. Recursing into children.')
            left = self.synchronize(origin, originnode.left, selfnode.left, 2 * index)
            right = self.synchronize(origin, originnode.right, selfnode.right, 2 * index + 1)
            return left + right
        else:
            print('   Resolving conflict at index {}.'.format(index))
            self.resolveconflict(origin, index)
            return [index]
    def resolveconflict(self, origin, index):
        if self.data[index].timestamp < origin.data[index].timestamp:
            self.data[index] = origin.data[index]
        else:
            origin.data[index] = self.data[index]

        self.computemerkle()
        origin.computemerkle()
    def __repr__(self):
        return str(self.data)

##########

# init parameters
datasize = 16
maxvalue = 1000

# color constants
white = [255, 255, 255]
black = [0, 0, 0]

# utility functions
def drawtext(text, loc):
    window.blit(font.render(text, True, black), loc)
    pygame.display.flip()

def drawdata(rep, loc):
    for datum in rep.data:
        pygame.draw.rect(window, black, [loc[0], loc[1], 30, 40], 1)
        drawtext(str(datum.datum), [loc[0] + 1, loc[1]])
        drawtext(str(datum.timestamp), [loc[0] + 1, loc[1] + 20])
        loc[0] += 30
    pygame.display.flip()

def drawnode(node, offset):
    x = offset[0] + 15 * (2**node.level - 1) + 30 * 2**node.level * node.index
    y = 600 - 100 * node.level
    pygame.draw.rect(window, white, [x, y, 30, 80]) # clear the previous node at this location (hacky)
    pygame.draw.rect(window, black, [x, y, 30, 80], 1)
    for chunk in [str(node.value)[i:i + 3] for i in range(0, len(str(node.value)), 3)]: # python is magical
        drawtext(chunk, [x + 1, y])
        y += 20
    pygame.display.flip()
    pygame.time.Clock().tick(10)

##########

import pygame
import random

# init pygame
pygame.init()
window = pygame.display.set_mode([1000, 750])
pygame.display.set_caption('AntiEntropy')
font = pygame.font.Font(pygame.font.match_font('inconsolata'), 18)
window.fill(white)

# test pairwise synchronization
testdata = {}
testdata['a'] = map(lambda d, t: Replica.Datum(d, t), map(str, random.sample(range(maxvalue), datasize)), random.sample(range(maxvalue), datasize))
testdata['b'] = list(testdata['a'])

conflicts = random.randint(0, datasize)
for x in random.sample(range(datasize), conflicts):
    testdata['b'][x] = Replica.Datum(random.randrange(maxvalue), random.randrange(maxvalue))

a = Replica(testdata['a'], [10, 0])
b = Replica(testdata['b'], [510, 0])

print('Data size: {}.'.format(datasize))
drawtext('Data size: {}.'.format(datasize), [0, 0])
print('Maximum data value: {}.'.format(maxvalue))
drawtext('Maximum data value: {}.'.format(maxvalue), [0, 20])
print('Number of conflicts: {}.'.format(conflicts))
drawtext('Number of conflicts: {}.'.format(conflicts), [0, 40])

print('')

print('--- Replica 1:')
print(a)
drawdata(a, [10, 700])
print('--- Replica 2:')
print(b)
drawdata(b, [510, 700])

print('')

print('--- Replica 1 Merkle Tree:')
a.computemerkle()
a.printmerkle()
print('--- Replica 2 Merkle Tree:')
b.computemerkle()
b.printmerkle()

print('')

indices = a.synchronize(b)

print('')

print('Replica 1 and Replica 2 were synchronized at indices {} ({} total).'.format(indices, len(indices)))

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
pygame.quit()

