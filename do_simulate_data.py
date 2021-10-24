from tsproperty import *
from tsgeneration import *
import sys
def main():
    # ----- Preparation ----- #
    prop=TSProperty()
    prop.set_par()

    # ----- Main ----- #
    gene=TSGeneration()
    gene.set_par(\
        dt=prop.dt,\
        n_bin=prop.n_bin,\
        n_seg=prop.n_seg,\
        name_outfile=prop.name_outfile)
    gene.set_property()
    psds=prop.set_psd(f=gene.fs)
    gene.set_psd(psd=psds)
    gene.print_info()
    gene.simulate_data()
    gene.write_data()

    print('Simulated data are stored in {0}.'.format(gene.name_outfile))
if __name__=='__main__':
    main()
