from MerkleReplica import MerkleReplica

# init parameters
datasize = 16
maxvalue = 1000

##########

import random

# test pairwise synchronization
testdata = {}
testdata['a'] = map(lambda d, t: MerkleReplica.Datum(d, t), map(str, random.sample(range(maxvalue), datasize)), random.sample(range(maxvalue), datasize))
testdata['b'] = list(testdata['a'])

conflicts = random.randint(0, datasize)
for x in random.sample(range(datasize), conflicts):
    testdata['b'][x] = MerkleReplica.Datum(random.randrange(maxvalue), random.randrange(maxvalue))

a = MerkleReplica(testdata['a'])
b = MerkleReplica(testdata['b'])

print('Data size: {}.'.format(datasize))
print('Maximum data value: {}.'.format(maxvalue))
print('Number of conflicts: {}.'.format(conflicts))

print('')

print('--- Replica 1:')
print(a)
print('--- Replica 2:')
print(b)

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
print('Network traffic cost: {}.'.format(a.networktraffic))
