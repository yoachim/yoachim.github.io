import numpy as np
import matplotlib.pylab as plt

countries = ['USA', r'Russia$^{\rm{**}}$', 'Canada', 'Mexico', 'Australia', 'Germany']
rates = [3.55, 9., 0.51, 10.0, 0.11, 0.20]

ind = np.arange(len(rates))
width = 0.35
fig, ax = plt.subplots()
rects = ax.bar(ind+width/2., rates, width)
ax.set_ylabel('Gun Homicide Rate (per 100,000)')
ax.set_xlabel('USA and Similar Countries')
ax.set_xticks(ind+width)
ax.set_xticklabels( countries )
rectsUS = ax.bar(ind[0]+width/2., rates[0], width, color='red')

fig.savefig('gunrate.png')
plt.close(fig)
