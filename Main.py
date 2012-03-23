from Replica import Replica
from NaiveReplica import NaiveReplica
from MerkleReplica import MerkleReplica

# init parameters
maxvalue = 1000
datacount = 32
testcount = 100

##########

import random

print('Data count: {}.'.format(datacount))
print('Maximum data value: {}.'.format(maxvalue))
print('Number of conflicts: {}.'.format(conflicts))

for conflicts in range(datacount):
    networktraffic = {}
    networktraffic['naive'] = []
    networktraffic['merkle'] = []

    for _ in range(testcount):
        testdata = {}
        testdata['a'] = map(lambda d, t: Replica.Datum(d, t), map(str, random.sample(range(maxvalue), datacount)), random.sample(range(maxvalue), datacount))
        testdata['b'] = list(testdata['a'])

        for x in random.sample(range(datacount), conflicts):
            testdata['b'][x] = Replica.Datum(random.randrange(maxvalue), random.randrange(maxvalue))

        a = NaiveReplica(list(testdata['a']))
        b = NaiveReplica(list(testdata['b']))

        indices = a.synchronize(b)

        # print('Naive scheme cost: {}.'.format(a.networktraffic))
        networktraffic['naive'].append(a.networktraffic)

        a = MerkleReplica(list(testdata['a']))
        b = MerkleReplica(list(testdata['b']))

        indices = a.synchronize(b)

        # print('Merkle tree-based scheme cost: {}.'.format(a.networktraffic))
        networktraffic['merkle'].append(a.networktraffic)

    print([sum(networktraffic[n], 0.0) / testcount for n in networktraffic])
