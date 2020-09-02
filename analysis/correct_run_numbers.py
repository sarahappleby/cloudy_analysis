import h5py
import numpy as np
import glob
import os
from shutil import copyfile

runParams = {}
runParams['densities'] = np.array([-9.   , -8.875, -8.75 , -8.625, -8.5  , -8.375, -8.25 , -8.125,
                                -8.   , -7.875, -7.75 , -7.625, -7.5  , -7.375, -7.25 , -7.125,
                                -7.   , -6.875, -6.75 , -6.625, -6.5  , -6.375, -6.25 , -6.125,
                                -6.   , -5.875, -5.75 , -5.625, -5.5  , -5.375, -5.25 , -5.125,
                                -5.   , -4.875, -4.75 , -4.625, -4.5  , -4.375, -4.25 , -4.125,
                                -4.   , -3.875, -3.75 , -3.625, -3.5  , -3.375, -3.25 , -3.125,
                                -3.   , -2.875, -2.75 , -2.625, -2.5  , -2.375, -2.25 , -2.125,
                                -2.   , -1.875, -1.75 , -1.625, -1.5  , -1.375, -1.25 , -1.125,
                                -1.   , -0.875, -0.75 , -0.625, -0.5  , -0.375, -0.25 , -0.125,
                                0.   ,  0.125,  0.25 ,  0.375,  0.5  ,  0.625,  0.75 ,  0.875,
                                1.   ,  1.125,  1.25 ,  1.375,  1.5  ,  1.625,  1.75 ,  1.875,
                                2.   ,  2.125,  2.25 ,  2.375,  2.5  ,  2.625,  2.75 ,  2.875,
                                3.   ,  3.125,  3.25 ,  3.375,  3.5  ,  3.625,  3.75 ,  3.875,
                                4.])

runParams['new_redshifts'] = np.array([0.     ,  0.12202,  0.25893,  0.41254,  0.58489,  0.77828,
                                0.99526,  1.2387 ,  1.5119 ,  1.8184 ,  2.1623 ,  2.5481 ,
                                2.9811 ,  3.4668 ,  4.0119 ,  4.6234 ,  5.3096 ,  6.0795 ,
                                6.9433 ,  7.9125 ,  9. ])

runParams['old_redshifts'] = np.array([0.     ,  0.12202,  0.25893,  0.41254,  0.58489,  0.77828,
                                0.99526,  1.2387 ,  1.5119 ,  1.8184 ,  2.1623 ,  2.5481 ,
                                2.9811 ,  3.4668 ,  4.0119 ,  4.6234 ,  5.3096 ,  6.0795 ,
                                6.9433 ,  7.9125 ,  9. , 10.22])

# For each file in original directory:
#   Read header, get density and redshift
#   Find number of this density and redshift by refering to list of possibilities
#   Write file to new file with correct name in a new directory


def get_old_run_number(run_dir, filename):
    basic_file = 'ion_fraction_FG19_run'
    pos = len(run_dir+basic_file)
    file_spec = filename[pos:]
    if ('warnings' in filename) or ('temp' in filename):
        return file_spec.split('.')[0]
    else:
        return file_spec.split('_')[0]

def get_hdens_and_z(runNo):
    nhdens = len(runParams['densities'])
    nredshift = len(runParams['old_redshifts'])

    hdens_no = int((runNo -1)/ nredshift)
    z_no = (runNo - 1) - (hdens_no * nredshift)
    return runParams['densities'][hdens_no], runParams['old_redshifts'][z_no]

def get_correct_run_number(hdens, z):
    # method to lookup true number of the density and redshift combo
    nhdens = len(runParams['densities'])
    nredshift = len(runParams['new_redshifts'])
    
    hdens_index = np.where(runParams['densities'] == hdens)[0] 
    z_index = np.where(runParams['new_redshifts'] == z)[0]

    correct_number = nredshift * hdens_index + z_index + 1.

    return int(correct_number)

def get_missing_runs():
    missing_runs_file = '/home/sapple/cloudy_analysis/ion_balance_tables/FG20_ion_fractions_missed_runs.dat'
    f = open(missing_runs_file, 'r')
    lines = f.readlines()
    f.close()
    return sorted([int(l) for l in lines])

if __name__ == '__main__':

    run_dir = '/home/sapple/cloudy_analysis/ion_balance_tables/ion_fraction_FG20_missing_runs/'
    out_dir = '/home/sapple/cloudy_analysis/ion_balance_tables/ion_fraction_FG20/'
    basic_file = 'ion_fraction_FG20_run'

    original_runs = 2310
    elements = ['Al', 'Ar', 'B', 'Be', 'Ca', 'C', 'Cl', 'Co', 'Cr', 'Cu', 'F', 'Fe', 'H', 'He', 
                'K', 'Li', 'Mg', 'Mn', 'Na', 'Ne', 'Ni', 'O', 'P', 'Sc', 'S', 'Si', 'Ti', 'V']

    missing_runs = get_missing_runs()

    run_strings = []
    for r in range(1, original_runs+1):
        if r in missing_runs:
            continue
        else:
            hdens, z = get_hdens_and_z(r)
            new_r = get_correct_run_number(hdens, z) 
           
            run_strings.append(str(new_r) + '\t' + str(hdens) + '\t' + '{:.4e}'.format(z) + '\n')

            for e in elements:
                old_file_name = basic_file + str(r) + '_'+ e +'.dat'
                new_file_name = basic_file + str(new_r) + '_'+ e +'.dat'
                copyfile(run_dir+old_file_name, out_dir+new_file_name)

    with open(out_dir+'ion_fraction_FG20.run', 'w') as f:
        f.writelines(run_strings)
