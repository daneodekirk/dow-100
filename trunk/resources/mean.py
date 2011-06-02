import math
import logging

class Mean:
    def __init__(self, data):
        self.data = data 

    def mean(self):
        """ This runs through the data set and calculates a
            running mean. Currently returns a 3-4 smooth.
        """
        #remove timestamp
        d = [ float(item[1]) for item in self.data]

        #mean over sets of 3 while checking the chunk size
        three = [ sum(d[i-1:i+2])/3 for i in range(len(d)) 
                    if len(d[i-1:i+2]) == 3 ] 
                
        #mean of the sets of 3 over sets of 4
        threefour = [ sum(three[i-1:i+3])/4 for i in range(len(three)) ] 

        #put timestamp back in 
        points = [ [self.data[i][0], threefour[i-1]]
                        for i in range(len(threefour)) ]

        #the first and last points seem chaotic
        points.pop(-1)
        points.pop(0)

        return points
