import numpy as np
import h5py
import pygad as pg

def roman_to_int(s):
    rom_val = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    int_val = 0
    for i in range(len(s)):
        if i > 0 and rom_val[s[i]] > rom_val[s[i - 1]]:
            int_val += rom_val[s[i]] - 2 * rom_val[s[i - 1]]
        else:
            int_val += rom_val[s[i]]
    return int_val

def get_species_info(line_list):
    lines = pg.analysis.absorption_spectra.lines
    elements = [lines[line]['element'] for line in line_list]
    ions = [lines[line]['ion'] for line in line_list]
    element_len = [len(element) for element in elements]
    ionisation = [ions[i][element_len[i]:] for i in range(len(ions))]
    ionisation = [roman_to_int(ion) for ion in ionisation]
    return elements, ionisation

def read_tnHz_from_h5(ion_file):
    with h5py.File(ion_file, 'r') as f:
        temps = f['temperature'][:]
        hdens = f['hydrogen_density'][:]
        redshifts = f['redshifts'][:]
    return temps, hdens, redshifts

def read_ions_from_h5(ion_file, line_list):
    
    elements, ionisations = get_species_info(line_list)

    fracs_dict = {}
    with h5py.File(ion_file, 'r') as f:
        for i in range(len(line_list)) :
            fracs_dict[line_list[i]] = f[elements[i]][:][ionisations[i] - 1]

    return fracs_dict

def interpolate():
    pass


if __name__ == '__main__':

    line_list = ['H1215']
    ion_file = '/home/sapple/ion_tables/FG20_ion_fractions.h5'

    fracs_dict = read_ions_from_h5(ion_file, line_list)
    temps, hdens, redshifts = read_tnHz_from_h5(ion_file)    
