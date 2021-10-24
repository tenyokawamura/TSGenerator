import numpy as np
from numpy import random
import astropy.io.fits as fits
import sys

class TSGeneration:
    def __init__(self):
        pass

    def set_par(self, dt, n_bin, n_seg, name_outfile):
        # Sampling interval
        self.dt=dt
        # Number of bins per segment
        self.n_bin=n_bin
        # Number of segments
        self.n_seg=n_seg
        # Output file name
        self.name_outfile=name_outfile

    def set_property(self):
        # Start time
        self.t_min=0
        # End time
        self.t_max=(self.n_bin-1)*self.dt
        # Total duration
        self.c_t=(self.t_max+self.dt)-self.t_min
        # Minimum frequency
        self.f_min=1./self.c_t
        # Maximum frequency
        self.f_max=1./(2.*self.dt)
        # Frequency interval
        self.df=self.f_min
        # Time
        #self.ts=t_min+self.dt*np.arange(self.n_bin)
        self.ts=np.arange(self.t_min, self.t_max+self.dt, self.dt)
        # Frequency
        self.fs=np.arange(self.f_min, self.f_max+self.df, self.df)

    def set_psd(self, psd):
        self.psds=psd
        if len(self.fs)!=len(self.psds):
            print('Error')
            sys.exit()

    def print_info(self):
        print('------------------------------')
        print('(Time series properties)')
        print('{0:<32}: {1:.2g}'.format('Timing intercal'           , self.dt))
        print('{0:<32}: {1}'    .format('Number of bins per segment', self.n_bin))
        print('{0:<32}: {1}'    .format('Total duration'            , self.c_t))
        print('{0:<32}: {1:.2g}'.format('Minimum frequency'         , self.f_min))
        print('{0:<32}: {1:.2g}'.format('Maximum frequency'         , self.f_max))
        print('{0:<32}: {1}'    .format('Number of segments'        , self.n_seg))
        print('{0:<32}: {1}'    .format('Output filename'           , self.name_outfile))
        print('')

    def simulate_data(self):
        for i_seg in range(self.n_seg):
            # Generate normalized Fourier coefficients
            bs_tilde=generate_fourier_coeffs(fs=self.fs, psds=self.psds)
            # Adjust Fourier coefficients
            bs=adjust_fourier_coeffs(bs_tilde=bs_tilde, dt=self.dt, n_bin=self.n_bin)
            # Inverse Fourier transform (Generate noise time series)
            xs=ifft_calc(bs=bs)
            if i_seg==0:
                self.xss=xs
            else:
                self.xss=np.vstack((self.xss, xs))

    def write_data(self):
        for i_seg in range(self.n_seg):
            hdu_ext=fits.BinTableHDU.from_columns([\
                fits.Column(name='TIME',   format='f4', array=self.ts),\
                fits.Column(name='DATA',   format='f4', array=self.xss[i_seg])])
            hdu_ext.header['TMIN']=(self.t_min, 'Start time')
            hdu_ext.header['TMAX']=(self.t_max, 'End time')
            hdu_ext.header['DT']  =(self.dt   , 'Timing interval')
            hdu_ext.header['T']   =(self.c_t  , 'Total duration')
            hdu_ext.header['NBIN']=(self.n_bin, 'Number of bin per segment')
            hdu_ext.header['FMIN']=(self.f_min, 'Minimum frequency')
            hdu_ext.header['FMAX']=(self.f_max, 'Maximum frequency')
            if i_seg==0:
                hdu_pri=fits.PrimaryHDU(data=None, header=None)
                hdus=fits.HDUList([hdu_pri, hdu_ext])
            else:
                hdus.append(hdu_ext)
        hdus.writeto(self.name_outfile, overwrite=True)

# Generate Fourier coefficients
def generate_fourier_coeffs(fs, psds):
    res=np.empty(0)
    ims=np.empty(0)
    mean=0
    for f, psd in zip(fs, psds):
        psd_uni=psd
        psd_bi=psd_uni/2. # unilateral --> bilateral
        sigma=np.sqrt(psd_bi/2.)
        re=random.normal(mean, sigma)
        im=random.normal(mean, sigma)
        res=np.append(res, re)
        ims=np.append(ims, im)
    bs_tilde=res+1j*ims
    return bs_tilde

# Adjust Fourier coefficients
def adjust_fourier_coeffs(bs_tilde, dt, n_bin): #For the use of numpy.fft.ifft
    bs_tilde_conju=bs_tilde.conjugate()
    if n_bin%2==0:
        bs_tilde_conju_flip=bs_tilde_conju[-2::-1]
    else:
        bs_tilde_conju_flip=bs_tilde_conju[-1::-1]
    bs=0.
    bs=np.append(bs, bs_tilde)
    bs=np.append(bs, bs_tilde_conju_flip)
    bs=bs*np.sqrt(n_bin/dt)
    return bs

# Inverse Fourier transform
def ifft_calc(bs):
    xs=np.fft.ifft(bs) #ifft has the normalization of 1/len(bs)
    xs=xs.real #Ideally Re[xs]=xs, Im[xs]=0
    return xs
