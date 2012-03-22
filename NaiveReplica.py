from Replica import Replica

class NaiveReplica(Replica):
    # initialize data
    def __init__(self, data=[]):
        # assumption (without loss of generality): data length must be power of 2
        self.data = data
        self.networktraffic = 0

    def synchronize(self, origin):
        indices = []
        for index in range(len(self.data)):
            self.networktraffic += 1
            if self.data[index].datum != origin.data[index].datum:
                # print('   Resolving conflict at index {}.'.format(index))
                indices.append(index)
                self.resolveconflict(origin, index)
        # print('   Conflict resolution complete.')
        return indices

    def resolveconflict(self, origin, index):
        if self.data[index].timestamp < origin.data[index].timestamp:
            self.data[index] = origin.data[index]
        else:
            self.networktraffic += 1
            origin.data[index] = self.data[index]
