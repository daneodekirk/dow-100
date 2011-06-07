import math
import logging

class Fourier:
    def __init__(self, data): 
        self.data = data

    def dft(self, inverse = False, verbose = False) :
        """ 
            Calculates the discrete fourier transform.
            Inspired by: 
            numericalrecipes.blogspot.com/2009/04/cooley-turkey-fft-algorithm.html

        """
        #remove timestamp
        x = [ float(item[1]) for item in self.data]

        N = len(x)
        inv = -1 if not inverse else 1
        X =[0] * N
        for k in xrange(N) :
            for n in xrange(N) :
                X[k] += x[n] * math.e**(inv * 2j * math.pi * k * n / N)
            if inverse :
                X[k] /= N
        #put timestamp back in 
        points = [ [self.data[i][0], X[i].real]
                        for i in range(len(X)) ]
        if verbose:
            logging.debug(points)
        return points
