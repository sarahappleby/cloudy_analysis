import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib import cm
import numpy as np
import h5py

num_map = [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), (90, 'XC'),
           (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]

def get_specexbin_nht():
    N_nh = 240 # number of nh gridpoints
    N_T = 140 # number of T gridpoints
    nh_low = -9.0
    T_low = 2.5
    delta_nh = 0.05
    delta_T = 0.05

    nh_array = np.arange(nh_low, nh_low + N_nh*delta_nh, delta_nh)
    T_array = np.arange(T_low, T_low + N_T*delta_T, delta_T)

    return nh_array, T_array 

def get_specexbin_ions(temp, nh_min, nh_max, ion):

    nh_array, T_array = get_specexbin_nht()

    temps_i = np.argmin(np.abs(T_array - temp))
    hdens_min_i = np.argmin(np.abs(nh_array - hdens_min))
    hdens_max_i = np.argmin(np.abs(nh_array - hdens_max))
    indices = [(i*len(T_array)) + temps_i for i in range(len(nh_array))]

    nh_plot = nh_array[hdens_min_i:hdens_max_i + 1]

    ion_file = '/home/rad/specexbin-phew/specexbin-phew-master/ionfiles/lt00HM12_i9'
    tbl = np.loadtxt(ion_file)

    if ion == 'HI': ion_index = 0
    elif ion == 'HeII': ion_index = 1
    elif ion == 'CIII': ion_index = 2
    elif ion == 'CIV': ion_index = 3
    elif ion == 'OIV': ion_index = 4
    elif ion == 'OVI': ion_index = 5
    elif ion == 'NeVIII': ion_index = 6
    elif ion == 'MgII': ion_index = 7
    elif ion == 'SiIV': ion_index = 8

    f = tbl[:, ion_index][indices][hdens_min_i:hdens_max_i + 1]

    return nh_plot, f

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

    backgrounds = ['fg20', 'no_uvb']
    temp = 5.5
    hdens_min = -4.
    hdens_max = -1.
    redshift = 0.
    linestyles = ['-', '--']
    uvb_labels = [r'${\rm FG20}$', r'${\rm No UVB}$']

    species = ['HI', 'MgII', 'SiIII', 'CIV', 'OVI']
    cmap = cm.get_cmap('viridis')
    dc = 1. / len(species)
    colors = [cmap((i+0.5) * dc) for i in range(len(species))]

    fig, ax = plt.subplots(1, 1, figsize=(6, 6))

    line_fg = Line2D([0,1],[0,1],ls=linestyles[0], marker=None, color='grey')
    line_no_uvb = Line2D([0,1],[0,1],ls=linestyles[1], marker=None, color='grey')
    leg_uvb = ax.legend([line_fg, line_no_uvb],uvb_labels, loc=3, fontsize=12)
    ax.add_artist(leg_uvb)

    # read in each of the ion table files for fg20, hm12-new and hm12-orig
    species_id = [0, 20, 25, 5, 15]
    for b, background in enumerate(backgrounds):
        if background == 'fg20':
            ion_table_file = '/disk04/sapple/ion_tables/FG20_oppenheimer_style/lt0000f100_i31'
            ions_start_from = 2
        elif background == 'hm12':
            ion_table_file = '/disk04/sapple/ion_tables/HM12_oppenheimer_style/lt0000f100_i31'
            ions_start_from = 2
        elif background == 'hm12_orig':
            ion_table_file = '/home/rad/pygad/iontbls/HM12/tbls-i31/lt00HM12_i31'
            ions_start_from = 0
        elif background == 'hm01':
            ion_table_file = '/home/rad/pygad/iontbls/tbls-i31/lt0000f100_i31'
            ions_start_from = 2
        elif background == 'no_uvb':
            ion_table_file = '/disk04/sapple/ion_tables/no_uvb_oppenheimer_style/lt0000f100_i31'
            ions_start_from = 2

        if background in ['fg20', 'hm12', 'hm01', 'no_uvb']:
            tbl = np.loadtxt(ion_table_file)
            nh_array = np.unique(tbl[:, 0])
            T_array = np.unique(tbl[:, 1])
            del tbl
        elif background in ['hm12_orig']:
            nh_array, T_array = get_specexbin_nht()

        T_i = np.argmin(np.abs(T_array - temp))
        nh_min_i = np.argmin(np.abs(nh_array - hdens_min))
        nh_max_i = np.argmin(np.abs(nh_array - hdens_max))
        indices = [(i*len(T_array)) + T_i for i in range(len(nh_array))]

        nh_plot = nh_array[nh_min_i:nh_max_i + 1]

        fion_tbl = np.loadtxt(ion_table_file)[:, ions_start_from:]
 
        for i, num in enumerate(species_id):
            frac_plot = fion_tbl[:, num][indices][nh_min_i:nh_max_i + 1]
            plt.plot(nh_plot, frac_plot, ls=linestyles[b], c=colors[i], label=species[i])
        if b == 0:
            plt.legend(fontsize=12, loc=4)
  
    """
    # Include the ion tables from specexbin (i9 style)
    ion_table_file_specexbin = '/home/rad/specexbin-phew/specexbin-phew-master/ionfiles/lt00HM12_i9'
    species_specexbin = ['HI', 'MgII', 'CIV', 'OVI']
    colors_specexbin = np.delete(colors, 2, axis=0)
    for i, ion in enumerate(species_specexbin):
        hdens_plot_specexbin, frac_plot_specexbin = get_specexbin_ions(temp, hdens_min, hdens_max, ion)
        plt.plot(hdens_plot_specexbin, frac_plot_specexbin, ls=linestyles[3], c=colors_specexbin[i])
    """

    plt.xlabel(r'${\rm log (nH)}$')
    plt.ylabel(r'${\rm log }(f_{\rm ion})$')
    plt.xlim(hdens_min, hdens_max)
    plt.ylim(-6, 0.5)

    plt.title(r'\textrm{log} (T / K) = '+str(temp))
    plt.savefig('ion_fracs_hdens.png')
    plt.close()
 

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


