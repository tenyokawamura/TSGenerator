import numpy as np

###################################################
##### Edit the class, TSProperty, as you want #####
###################################################
class TSProperty:
    def __init__(self):
        pass

    def set_par(self):
        # Sampling interval
        self.dt=1.
        # Number of bins per segment
        self.n_bin=2**10
        # Number of segments
        self.n_seg=10
        # Output file name
        self.name_outfile='time_series.fits'
        
    def set_psd(self, f):
        psd=1./f
        return psd

