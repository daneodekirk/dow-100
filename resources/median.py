import math

class Median:
    def __init__(self, data, s=3):
        self.data = data 
        self.chunk = s
    
    def average(self, i):
        s = int(math.floor(self.chunk/2))
        s2 = s+1

        info = self.data[i-s2:i+s]
        time = self.data[i][0]

        del self.data[i-s2:i+s]

        points = [float(item[1]) for item in info]
        added = sorted(points)
        if len(added) > 0:
            logging.debug(added[-1])
            added = added[-1]

        #return [time, added/self.chunk]
        return [time, added]


    def endpoint(self, i):
        n = 1 if i == 0 else -1
        #note: weighted value is already a median
        f1, g1, g2 = self.data[i][0], self.data[i+n][0], self.data[i+(2*n)][0]
        return sorted([f1, g1, (3 * g1 - 2 * g2)])[1]

    def median(self):
        medians = [ self.average(i) for i in range(len(self.data)) 
                        if 0 < i < len(self.data)-1 ] 

        #medians[0][0] = self.endpoint(0)
        #medians[-1][0] = self.endpoint(len(medians) - 1)
        return medians

