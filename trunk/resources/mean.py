import math

class Mean:
    def __init__(self, data):
        self.data = data 
        self.cache = []
        self.output = []
    
    def threes(self, i, s):
        info = self.data[i:i+3]
        time = self.data[i][0]

        points = [float(item[1]) for item in info]
        added = sum(points)/3

        self.cache.append([time, added])

        return [time, added]

    def fours(self, i, s):
        info = self.cache[i:i+4]
        time = self.cache[i][0]

        points = [item[0] for item in info]
        added = sum(points)/4

        self.output.append([added, time])

        return [time, added]

    def mean(self):
        data = [ self.threes(i, 3) for i in range(len(self.data)) 
                        if 0 < i < len(self.data)-1 ] 
        return data
        #[TODO] Four smoothing causing an error
        #newdata = [ self.fours(i, 3) for i in range(len(data)) 
                        #if 0 < i < len(data)-1 ] 
