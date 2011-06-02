import math
import logging

class Median:
    def __init__(self, data, s=3):
        self.data = data 
        self.chunk = s

    def endpoint(self, i):
        """ Caculates the endpoints of the running median 
            based on the assumption of using chunks of 3
        """
        
        n = 1 if i == 0 else -1
        #note: weighted value is already a median
        f1, g1, g2 = self.data[i][0], self.data[i+n][0], self.data[i+(2*n)][0]
        return sorted([f1, g1, (3 * g1 - 2 * g2)])[1]

    def median(self):
        """ This runs through the data set and orders by medians.
            Currently uses sets of three.
        """
        
        #remove the time domain
        d = [item[1] for item in self.data]

        #resort as medians
        medians = [ sorted(d[i-1:i+2])[1] for i in range(len(d))
                        if 0 < i < len(d)-1 ] 
        #put time domain back in
        points = [ [self.data[i+1][0], medians[i] ] 
                        for i in range(len(medians)) ]

        return points

