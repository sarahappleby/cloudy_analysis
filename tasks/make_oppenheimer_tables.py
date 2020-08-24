import h5py
import numpy as np

def format_redshift(z):
    z = "{:.3f}".format(z)
    dec = z.find('.')
    if dec == 1:
        z = '0' + z
    z = z.replace('.', '')
    return z

def make_lines_from_array(array):
    lines = []
    for i in range(len(array)):
        line = ['%s' % float('%.5g' % x) for x in array[i]]
        lines.append(('\t').join(line) + '\n')
    return lines

header = '#Hdens  Temp    HydrogenI HeliumI   HeliumII  CarbonII  CarbonIII CarbonIV  CarbonV   NitrogeIV NitrogenV NitrogeVI OxygenI   OxygenII  OxygenIII OxygenIV  OxygenV   OxygenVI  OxygenVII OxygeVIII NeonIV    NeonVIII  MagnesiII MagnesiuX AluminuII AluminIII SiliconII SilicoIII SiliconIV SilicoXII CarbonVI  NeonIX    IronII    redshift= '

elements = ['H', 'He', 'C', 'N', 'O', 'Ne', 'Mg', 'Al', 'Si', 'C', 'Ne', 'Fe']
species = [[1], [1, 2], [2, 3, 4, 5], [4, 5, 6], 
           [1, 2, 3, 4, 5, 6, 7, 8], [4, 8], [2, 10],
           [2, 3], [2, 3, 4, 12], [6], [9], [2]]

Nspecies = sum(len(species[i]) for i in range(len(species)))

ion_table_file = '/home/sapple/ion_tables/FG20_ion_fractions.h5'
with h5py.File(ion_table_file, 'r') as itf:
    redshifts = itf['redshifts'][:]
    
    temps = itf['temperature'][:]
    hdens = itf['hydrogen_density'][:]

    temps_array = np.tile(temps, len(hdens))
    hdens_array = np.repeat(hdens, len(temps))

    for i, redshift in enumerate(redshifts):
       
        redshift_string = format_redshift(redshift)
        new_table_file = '/home/sapple/ion_tables/FG20_oppenheimer_style/lt'+redshift_string+'f100_i'+str(Nspecies)


        ion_fractions = np.zeros((Nspecies+2, len(temps_array)))
        ion_fractions[0] = hdens_array.copy()
        ion_fractions[1] = temps_array.copy()

        j = 2
        for k, e in enumerate(elements): 
            for ion in species[k]:
                # for each hydrogen density, get the fractions for every temperature
                ion_fractions[j] = itf[e][:][ion - 1][:, i].flatten()
                j += 1

        ion_fractions = np.transpose(ion_fractions)

        lines = make_lines_from_array(ion_fractions)
        lines.insert(0, header+"{:.5f}".format(redshift) + '\n')

        with open(new_table_file, 'w') as ntf:
            ntf.writelines(lines)

        del lines, ion_fractions
