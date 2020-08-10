# Adapted from a script by Britton Smith for use with the latest FG20 file format.
# Puts the FG20 data into the format required for Britton's Cloudy tools.

import numpy as np
import h5py
import os

tiny_number = 1e-50
l_tiny = np.log10(tiny_number)

planck_constant_cgs   = 6.62606896e-27  # erg s
speed_of_light_cgs = 2.99792458e10
Ryd_to_erg = 13.60569253 * 1.60217646e-12


def read_UVB_data_FG(input_file):
    print("Loading Faucher-Giguere data from %s." % input_file)

    redshift = None
    intro_lines = []
    energy = []
    jnu = []

    lines = open(input_file, 'r').readlines()
    
    # previously, for the cloudy format file, we had commented intro lines. We don't use this now for the
    # normal redshift + energy, spectrum files.

    #for line in lines:
    #    if line.startswith('#'):
    #        continue
    #    if len(line) < 100.:
    #        intro_lines.append(line)
    #    elif (len(line) > 100) & (len(line) < 1000):
    #        redshift = [float(i) for i in line.split()]
    #    else:
    #        my_energy = line.split()[0]
    #        energy.append(float(my_energy))
    #
    #        my_jnu = line[len(my_energy) + 3:]
    #        jnu.append([float(i) for i in my_jnu.split()])

    for i, line in enumerate(lines):
        if i == 0:
            redshift = [float(i) for i in line.split()]
        else:
            my_energy = line.split()[0]
            energy.append(float(my_energy))

            my_jnu = line[len(my_energy) + 3:]
            jnu.append([float(i) for i in my_jnu.split()])

    redshift = np.array(redshift)
    energy = np.array(energy)
    jnu = np.log10(jnu)
    jnu -= 21.0 # convert from 10^-21 erg s^-1 cm^-2 Hz^-1 sr^-1

    jnu = np.transpose(np.array(jnu))

    my_sort = redshift.argsort()
    redshift = redshift[my_sort]
    jnu = jnu[my_sort]

    return (redshift, energy, jnu)

def create_interpolated_spectrum(redshift, jnu, my_redshift):
    indices = np.digitize(my_redshift, redshift)
    indices = np.clip(indices, a_min=1, a_max=redshift.size-1)
    slope = (jnu[indices, :] - jnu[indices-1, :]) / \
      (redshift[indices] - redshift[indices-1])
    values = slope * (my_redshift - redshift[indices]) + jnu[indices, :]
    return values


def write_spectrum_table(output_file, redshift, energy, ljnu,
                         reverse=True):

    my_energy = np.copy(energy)
    my_ljnu = np.copy(ljnu)

    e_min = 1.001e-8
    e_max = 7.354e6
    if reverse:
        my_energy = my_energy[::-1]
        my_ljnu = my_ljnu[::-1]
    my_energy = np.concatenate([[0.99 * my_energy[0]],
                                my_energy,
                                [1.01 * my_energy[-1], e_max]])
    my_ljnu = np.concatenate([l_tiny * np.ones(1),
                              my_ljnu,
                              l_tiny * np.ones(2)])

    print("Writing spectrum for z = %f to %s." % (redshift, output_file))
    out_file = open(output_file, 'w')
    out_file.write("# Faucher-Giguere 2019 \n")
    out_file.write("# z = %f\n" % redshift)
    out_file.write("# E [Ryd] log (J_nu)\n")
    out_file.write("interpolate (%.16f %.16f)\n" % \
                   (e_min, np.log10(tiny_number)))
    for i, e in enumerate(my_energy):
        if my_energy[i] == my_energy[i-1]:
            e *= 1.0001
        out_file.write("continue (%.16f %.16f)\n" % (e, my_ljnu[i]))

    my_e = 1.0
    e_value = np.log10(my_e)
    my_energy = np.log10(my_energy)
    index = np.digitize([e_value], my_energy)[0]
    slope = (my_ljnu[index] - my_ljnu[index - 1]) / \
      (my_energy[index] - my_energy[index - 1])
    my_j = slope * (e_value - my_energy[index]) + my_ljnu[index]
    my_j += np.log10(4 * np.pi)
    out_file.write("f(nu) = %.16f at %.16f Ryd\n" % \
                   (my_j, my_e))
    out_file.close()


def write_spectra(redshift, energy, ljnu,
                  output_redshift, output_dir,
                  reverse=True):

    if not os.path.exists(output_dir): os.mkdir(output_dir)
    for z in output_redshift:
        output_file = os.path.join(output_dir,
                                   "z_%10.4e.out" % z)
        my_spec = create_interpolated_spectrum(redshift, ljnu, [z])
        write_spectrum_table(output_file, z, energy, my_spec[0],
                             reverse=reverse)


if __name__ == '__main__':

    my_dlx = 0.05
    fg19_file = '/home/sapple/fg20_031220/fg20_spec_nu.dat'
    save_dir = '/home/sapple/cloudy_analysis/FG20_UVB/'

    redshift_fg, energy_fg, ljnu_fg = read_UVB_data_FG(fg19_file)
    my_lx = np.arange(np.log10(redshift_fg[0]+1),
                      np.log10(redshift_fg[-1]+1), my_dlx)
    my_redshift = np.power(10, my_lx) - 1
    write_spectra(redshift_fg, energy_fg, ljnu_fg,
                  my_redshift, "FG20_UVB", reverse=False)

