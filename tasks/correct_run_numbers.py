import h5py
import numpy as np
import glob
import os

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

runParams['redshifts'] = np.array([0.     ,  0.12202,  0.25893,  0.41254,  0.58489,  0.77828,
                                0.99526,  1.2387 ,  1.5119 ,  1.8184 ,  2.1623 ,  2.5481 ,
                                2.9811 ,  3.4668 ,  4.0119 ,  4.6234 ,  5.3096 ,  6.0795 ,
                                6.9433 ,  7.9125 ,  9. ])

# For each file in original directory:
#   Read header, get density and redshift
#   Find number of this density and redshift by refering to list of possibilities
#   Write file to new file with correct name in a new directory

def read_header():
    # method to read header and get the density and redshift
    pass

def get_old_run_number(run_dir, filename):
    basic_file = 'ion_fraction_FG19_run'
    pos = len(run_dir+basic_file)
    file_spec = filename[pos:]
    if ('warnings' in filename) or ('temp' in filename):
        return file_spec.split('.')[0]
    else:
        return file_spec.split('_')[0]

def get_correct_run_number():
    # method to lookup true number of the density and redshift combo
    pass

def write_to_file():
    # method to write new file
    pass

if __name__ == '__main__':

    run_dir = '/home/sapple/cloudy_analysis/ion_balance_tables/ion_fraction_FG19_missing_z/'
    out_dir = '/home/sapple/cloudy_analysis/ion_balance_tables/ion_fraction_FG19/'

    basic_file = 'ion_fraction_FG19_run'

    all_files = sorted(glob.glob(run_dir+'*'))

    for f in all_files:
        runNo = get_old_run_number(run_dir, f)
        

