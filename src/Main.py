from Replica import Replica
from NaiveReplica import NaiveReplica
from MerkleReplica import MerkleReplica

# init parameters
maxvalue = 1000
datacount = 32
samplesize = 100

##########

import random

print('Data count: {}.'.format(datacount))
print('Maximum data value: {}.'.format(maxvalue))
print('Sample size: {}.'.format(samplesize))

for conflicts in range(datacount):
    networkusage = {}
    networkusage['naive'] = []
    networkusage['merkle'] = []

    for _ in range(samplesize):
        testdata = {}
        testdata['a'] = map(lambda d, t: Replica.Datum(d, t), map(str, random.sample(range(maxvalue), datacount)), random.sample(range(maxvalue), datacount))
        testdata['b'] = list(testdata['a'])

        for x in random.sample(range(datacount), conflicts):
            testdata['b'][x] = Replica.Datum(random.randrange(maxvalue), random.randrange(maxvalue))

        a = NaiveReplica(list(testdata['a']))
        b = NaiveReplica(list(testdata['b']))

        indices = a.synchronize(b)

        # print('Naive scheme cost: {}.'.format(a.networkusage))
        networkusage['naive'].append(a.networkusage)

        a = MerkleReplica(list(testdata['a']))
        b = MerkleReplica(list(testdata['b']))

        indices = a.synchronize(b)

        # print('Merkle tree-based scheme cost: {}.'.format(a.networkusage))
        networkusage['merkle'].append(a.networkusage)

    print([sum(networkusage[n], 0.0) / samplesize for n in networkusage])
