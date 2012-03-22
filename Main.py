from Replica import Replica
from NaiveReplica import NaiveReplica
from MerkleReplica import MerkleReplica

# init parameters
datasize = 16
maxvalue = 1000

##########

import random

# test pairwise synchronization
testdata = {}
testdata['a'] = map(lambda d, t: Replica.Datum(d, t), map(str, random.sample(range(maxvalue), datasize)), random.sample(range(maxvalue), datasize))
testdata['b'] = list(testdata['a'])

conflicts = random.randint(0, datasize)
# conflicts = 0
for x in random.sample(range(datasize), conflicts):
    testdata['b'][x] = Replica.Datum(random.randrange(maxvalue), random.randrange(maxvalue))

print('Data size: {}.'.format(datasize))
print('Maximum data value: {}.'.format(maxvalue))
print('Number of conflicts: {}.'.format(conflicts))

print('')

# print('--- Replica 1:')
# print(testdata['a'])
# print('--- Replica 2:')
# print(testdata['b'])

# print('')

a = NaiveReplica(list(testdata['a']))
b = NaiveReplica(list(testdata['b']))

print('--- Naive scheme:')

indices = a.synchronize(b)

print('Replica 1 and Replica 2 were synchronized at indices {} ({} total).'.format(indices, len(indices)))
print('Network traffic cost: {}.'.format(a.networktraffic))

print('')

a = MerkleReplica(list(testdata['a']))
b = MerkleReplica(list(testdata['b']))

# print('--- Replica 1 Merkle Tree:')
# a.computemerkle()
# a.printmerkle()
# print('--- Replica 2 Merkle Tree:')
# b.computemerkle()
# b.printmerkle()

# print('')

print('--- Merkle tree-based scheme:')

indices = a.synchronize(b)

print('Replica 1 and Replica 2 were synchronized at indices {} ({} total).'.format(indices, len(indices)))
print('Network traffic cost: {}.'.format(a.networktraffic))

print('')
