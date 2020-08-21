import matplotlib.pyplot as plt
import numpy as np
import h5py

num_map = [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), (90, 'XC'),
           (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]

def num2roman(num):
    roman = ''
    while num > 0:
        for i, r in num_map:
            while num >= i:
                roman += r
                num -= i
    return roman

if __name__ == '__main__':

    background = 'fg20'
    temp = 4.
    hdens_min = -4.
    hdens_max = -1.
    redshift = 0.

    # plot from the oppenheimer tables:
    species = ['H1215', 'CIV1548', 'OVI1031', 'MgII2796', 'SiIII1206']
    if background == 'fg20':
        ion_table_file = '/home/sapple/ion_tables/FG20_oppenheimer_style/lt00000f100_i31'
        species_id = [2, 7, 18, 24, 29]
    elif background == 'hm12':
        ion_table_file = '/home/rad/pygad/iontbls/tbls-i31/lt00000f100_i31'
        species_id = [2, 7, 17, 22, 27]
    #read in the text file, get the ion we want, select a temperature
    
    tbl = np.loadtxt(ion_table_file)

    hdens = np.unique(tbl[:, 0])
    temps = np.unique(tbl[:, 1])

    temps_i = np.argmin(np.abs(temps - temp))
    hdens_min_i = np.argmin(np.abs(hdens - hdens_min))
    hdens_max_i = np.argmin(np.abs(hdens - hdens_max))

    indices = [(i*len(temps)) + temps_i for i in range(len(hdens))]

    hdens_plot = hdens[hdens_min_i:hdens_max_i + 1]

    for i, num in enumerate(species_id):

        frac_plot = tbl[:, num][indices][hdens_min_i:hdens_max_i + 1]
        plt.plot(hdens_plot, frac_plot, label=species[i])

    plt.legend()
    plt.xlabel('log (nH)')
    plt.ylabel('log (ion fraction)')
    plt.savefig('./plots/'+background+'_hdens_ion_fracs.png')
    plt.clf()
 

    # plot from the h5 file:
    """
    temp = 4.
    hdens_min = -4.
    hdens_max = -1.
    redshift = 0.

    species = {'H': [1], 'C': [4], 'O': [6], 'Mg': [2], 'Si':[3]}
    elements = species.keys()

    ion_table_file = '/home/sapple/ion_tables/FG20_ion_fractions.h5'
    with h5py.File(ion_table_file, 'r') as itf:
    
        redshifts = itf['redshifts'][:]
        temps = itf['temperature'][:]
        hdens = itf['hydrogen_density'][:]

        redshift_i = np.argmin(np.abs(redshifts - redshift))
        temps_i = np.argmin(np.abs(temps - temp))
        hdens_min_i = np.argmin(np.abs(hdens - hdens_min))
        hdens_max_i = np.argmin(np.abs(hdens - hdens_max))

        hdens_plot = hdens[hdens_min_i:hdens_max_i + 1]

        for e in elements:
            for ion in species[e]:

                fracs = itf[e][:][ion - 1][:, redshift_i]
                fracs_plot = fracs[:, temps_i][hdens_min_i:hdens_max_i + 1]

                plt.plot(hdens_plot, fracs_plot, label=e + num2roman(ion))

        plt.legend()
        plt.xlabel('log (nH)')
        plt.ylabel('log (ion fraction)')
        plt.savefig('./plots/hdens_ion_fracs.png')
        plt.clf()
        """ 


