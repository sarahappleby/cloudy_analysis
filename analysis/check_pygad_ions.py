import numpy as np
import pygad as pg

model = 'm100n1024'
wind = 's50'
snap = '151'
survey = 'dwarfs'

T_choose = 4.0
nh_choose = -6.0
dt = 0.05
dnh = 0.05

all_ions = ['HI', 'HeI', 'HeII', 'CII', 'CIII', 'CIV', 'CV', 'NIV', 'NV', 'NVI',
        'OI', 'OII', 'OIII', 'OIV', 'OV', 'OVI', 'OVII', 'OVIII', 'NeIV', 'NeVIII',
        'MgII', 'MgX', 'AlII', 'AlIII', 'SiII', 'SiIII', 'SiIV', 'SiXII', 'CVI',
        'NeIX', 'FeII']
ions_i = [0, 20, 25, 5, 15] # indices of our ions in the above list
ions_el = ['H', 'Mg', 'Si', 'C', 'O']
ions_state = ['I', 'II', 'III', 'IV', 'VI']

# load in the oppenheimer table
tbl_file = '/home/sapple/ion_tables/FG20_oppenheimer_style/lt00000f100_i31'
tbl = np.loadtxt(tbl_file)

# find indices for the temp and nh
nh_tbl = np.unique(tbl[:, 0])
temp_tbl = np.unique(tbl[:, 1])
temp_i = np.argmin(np.abs(temp_tbl - T_choose))
nh_i = np.argmin(np.abs(nh_tbl - nh_choose))

# get the fracs for the selected ions
entry = tbl[:][nh_i * len(temp_tbl) + temp_i]
line_ions = ''
line_tbl = ''
for i in ions_i:
    line_ions += all_ions[i] + '\t'
    line_tbl += str(entry[2+i])+'\t'

# next, get the same thing from pygad:
snapfile = '/home/sapple/cgm/cos_samples/'+model+'/cos_'+survey+'/samples/'+model+'_'+wind+'_'+snap+'.hdf5'
s = pg.Snapshot(snapfile)

# get a mask for the particles at chosen T and nH
temp_pg = np.log10(s['temp'])
nh_pg = np.log10(s['nh'])
mass_pg = s['mass'].in_units_of('Msol')
temp_pg_mask = (temp_pg < (T_choose + dt)) & (temp_pg > (T_choose - dt))
nh_pg_mask = (nh_pg < (nh_choose + dnh)) & (nh_pg > (nh_choose - dnh))
mask = temp_pg_mask * nh_pg_mask

# get the fracs from pygad calculations:
line_pg = ''
for i in range(len(ions_el)):

    ion_mass = s.gas.get(ions_el[i]).in_units_of('1e+10 Msol h_0**-1')
    if ions_el == 'H':
        f_ion = pg.snapshot.derived.derive_rules.calc_HI_mass(s)[mask].in_units_of('1e+10 Msol h_0**-1') / ion_mass[mask]
    else:
        f_ion = pg.snapshot.derived.derive_rules.calc_ion_mass(s, ions_el[i], ions_state[i])[mask].in_units_of('1e+10 Msol h_0**-1') / ion_mass[mask]

    f_ion = float(np.nanmedian(np.log10(f_ion)))
    line_pg += str(round(f_ion, 3)) + '\t'

print('\nlog T = '+str(T_choose))
print('log nH = '+str(nh_choose))
print('Chosen ions: ')
print(line_ions)
print('Ion fractions from Oppenheimer table: ')
print(line_tbl)
print('Ion fractions from pygad: ')
print(line_pg)

