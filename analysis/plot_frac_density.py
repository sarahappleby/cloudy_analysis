import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib import cm
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

plt.rc('text', usetex=True)
plt.rc('font', family='serif', size=14)

if __name__ == '__main__':

    backgrounds = ['fg20', 'hm12']
    temp = 4.
    hdens_min = -4.
    hdens_max = -1.
    redshift = 0.
    linestyles = ['-', '--']
    uvb_labels = [r'$\textrm{FG20}$', r'$\textrm{HM12}$']

    species = ['HI', 'MgII', 'SiIII', 'CIV', 'OVI']
    cmap = cm.get_cmap('viridis')
    dc = 1. / len(species)
    colors = [cmap((i+0.5) * dc) for i in range(len(species))]

    fig, ax = plt.subplots(1, 1, figsize=(6, 6))

    line_fg = Line2D([0,1],[0,1],ls=linestyles[0], marker=None, color='grey')
    line_hm = Line2D([0,1],[0,1],ls=linestyles[1], marker=None, color='grey')

    leg_uvb = ax.legend([line_fg, line_hm],uvb_labels, loc=3, fontsize=12)
    ax.add_artist(leg_uvb)

    for b, background in enumerate(backgrounds):
        if background == 'fg20':
            ion_table_file = '/home/sapple/ion_tables/FG20_oppenheimer_style/lt00000f100_i31'
        elif background == 'hm12':
            ion_table_file = '/home/rad/pygad/iontbls/tbls-i31/lt00000f100_i31'
        species_id = [2, 22, 27, 7, 17]

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
            plt.plot(hdens_plot, frac_plot, ls=linestyles[b], c=colors[i], label=species[i])
        if b == 0:
            plt.legend(fontsize=12)
            ax.set_xlabel(r'${\rm log (nH)}$')
            ax.set_ylabel(r'${\rm log }(f_{\rm ion})$')
            ax.set_xlim(hdens_min, hdens_max)
            ax.set_ylim(-6, 0.5)
    
    plt.savefig('./plots/hdens_ion_fracs.png')
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


