import glob

outfile = '/home/sapple/cloudy_analysis/missed_runs.dat'

files = sorted(glob.glob('/home/sapple/cloudy_analysis/ion_balance_tables/ion_fraction_FG20/*'))

prefix = '/home/sapple/cloudy_analysis/ion_balance_tables/ion_fraction_FG20/ion_fraction_FG20_run'

missed_runs = []

for f in files:
    open_file = open(f, 'r') 
    lines = open_file.readlines()
    open_file.close()

    if len(lines) < 15:
        name = f[len(prefix):].split('_')[0]
        missed_runs.append(name)
        print('Missed run '+ name)

unique = set(missed_runs)
new_values = []
for value in unique:
    if not 'cloudyIn.temp' in value:
        new_values.append(value)
new_values = sorted(new_values)

with open(outfile, 'w') as o:
    for value in new_values:
        o.write("{}\n".format(value))
