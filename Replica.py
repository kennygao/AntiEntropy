class Replica:
    class Datum:
        def __init__(self, datum, timestamp):
            self.datum = datum
            self.timestamp = timestamp
        def __repr__(self):
            return str((self.datum, self.timestamp))

    # initialize data
    def __init__(self, data=[]):
        # assumption (without loss of generality): data length must be power of 2
        self.data = data

    def __repr__(self):
        return str(self.data)

