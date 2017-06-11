import numpy as np
import pandas as pd
import matplotlib.pylab as plt
from matplotlib_venn import venn3_circles, venn3


def read_simp(filename):
    result = []
    with open(filename) as f:
        content = f.readlines()
    for line in content:
        line = line.split('  ')
        result.append(line[1].strip())
    return result


def read_fg(filename):
    result = []
    with open(filename) as f:
        content = f.readlines()
    for line in content:
        line = line.split('  ')
        result.append(line[0].strip())
    return result

fg = read_fg('familyGuy.dat')
simp = read_simp('simpsons.dat')

sf = pd.read_csv('super.dat').values
sf = [row[0] for row in sf]



venn3([set(simp), set(fg), set(sf)], ('Simpsons', 'Family Guy', 'Super Friends'))
plt.title('Celebrity Cartoon Voices')
plt.savefig('west_venn.png')

