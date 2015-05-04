import numpy as np
import matplotlib.pylab as plt

names = ['Drive & Park', 'Car2Go', 'Bus', 'Bike']
costs = [6/2 , 13.*.41, 2.25, 0.]
times = [ 10+15, 15,25,23 ]
ptcolors = ['yellow', 'blue', 'black', 'green']
xoffs = [-20,40,-20,-20]
yoffs = [0,20,0,0]

fig = plt.figure()
ax=fig.add_subplot(111)
for x,y,c in zip(times, costs,ptcolors):
    ax.plot(x,y,color=c, marker='o', markersize=12)
ax.set_xlabel('Time (minutes)')
ax.set_ylabel('Cost ($)')
ax.set_title('Work Commute Options')
ax.set_ylim([0,10])

for label,x,y,c,xoff,yoff in zip(names,times,costs, ptcolors,xoffs,yoffs):
    ax.annotate(label, xy=(x,y), xytext=(xoff,yoff),
                textcoords = 'offset points', ha = 'right', va = 'bottom',
                bbox = dict(boxstyle = 'round,pad=0.5', fc = c, alpha = 0.1)
                )



plt.savefig('towork.png')
