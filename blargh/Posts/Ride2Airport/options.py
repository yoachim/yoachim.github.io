import numpy as np
import matplotlib.pylab as plt

names = ['Taxi', 'UberX', 'Drive & Park', 'Car2Go (if I could park it!)', 'Bus & Rail']
costs = [71, 42, 37, 12, 5.5]
times = [40,40,40,30,78]
ptcolors = ['yellow', 'black', 'red', 'blue', 'green']

xoffs = [-20,-20,90,90,-20]
yoffs = [0,0,0,-30,0]

fig = plt.figure()
ax=fig.add_subplot(111)
for x,y,c in zip(times, costs,ptcolors):
    ax.plot(x,y,color=c, marker='o', markersize=12)
ax.set_xlabel('Time (minutes)')
ax.set_ylabel('Cost ($)')
ax.set_title('Getting To the Airport')
ax.set_xlim([20,80])

for label,x,y,c,xoff,yoff in zip(names,times,costs, ptcolors,xoffs,yoffs):
    ax.annotate(label, xy=(x,y), xytext=(xoff,yoff),
                textcoords = 'offset points', ha = 'right', va = 'bottom',
                bbox = dict(boxstyle = 'round,pad=0.5', fc = c, alpha = 0.1)
                )



plt.savefig('options.png')
#plt.show()
