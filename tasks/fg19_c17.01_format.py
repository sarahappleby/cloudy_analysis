import numpy as np

fg19_file = '/home/sapple/c17.01/data/hm12_galaxy_errors.ascii'
save_file = '/home/sapple/c17.01/data/hm12_galaxy.ascii'

separator = '  '

intro_lines = []
redshift_line = ''
spectra = []

wave_line = ''
j = 1

def get_nice_lines(line, n):
    new_lines = []
    new_line = ''
    split = line.split('  ')
    for i in list(range(len(split))):
        if ('\n' in split[i]) or (len(split[i]) == 0.):
            continue
        new_line += split[i] + '  '
        if ((i + 1) % n) == 0.:
            new_lines.append(new_line + '\n')
            new_line = ''
    new_lines.append(new_line + '\n')
    return new_lines


f = open(fg19_file, 'r')

for line in f.readlines():
    if line[0] == '#':
        continue
    if len(line) < 100:
        intro_lines.append(line)
    elif (len(line) > 100) & (len(line) < 1000):
        redshift_line = line + ''
    else:
        wave = line.split(' ')[0]
        line = line[len(wave) + 3:]
        spectra.append([float(i) for i in line.split('  ')[:-1]])
        wave_line += wave + '  '

f.close()

spectra = np.transpose(np.array(spectra))
spectrum_lines = []
for s in spectra:
    in_string = ['%.5e' % i for i in s]
    in_string = separator.join(in_string) + '  \n'
    spectrum_lines.append(in_string)

redshift_line = get_nice_lines(redshift_line, 10)
wavelength_lines = get_nice_lines(wave_line, 8)

all_lines = intro_lines + redshift_line + wavelength_lines

for l in spectrum_lines:
    all_lines += get_nice_lines(l, 10)

with open(save_file, 'w') as s:
    for line in all_lines:
        s.write(line)
