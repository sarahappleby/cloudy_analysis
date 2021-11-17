import sys

if __name__ == '__main__':

    orig_filename = sys.argv[1]
    new_filename = sys.argv[2]

    with open(orig_filename) as file:
        lines = file.readlines()

    new_lines = lines.copy()

    for l in range(len(new_lines)):
        line = new_lines[l]
        if line[0] == '#': continue

        line_parts = line.split()
        if line_parts[0] == 'f(nu)':continue

        spec = float(line_parts[-1][:-1])

        line_parts[-1] = '{0:.16f}'.format(spec*1e-10) + ')'
        new_lines[l] = ' '.join(line_parts) + '\n'

    
    with open(new_filename, 'w') as outfile: 
        for line in new_lines:
            outfile.write(line)
