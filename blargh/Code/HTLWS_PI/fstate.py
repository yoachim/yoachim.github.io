#grabbed from http://nbviewer.ipython.org/urls/raw.github.com/rdhyee/working-open-data/master/notebooks/Day_14_basemap_redux.ipynb

from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap as Basemap
from matplotlib.colors import rgb2hex
from matplotlib.patches import Polygon
import matplotlib as mpl
import numpy as np
import numpy.lib.recfunctions as nprf



names=['state','homicides', 'gun_rate', 'auto_rate']
types=['|S20', 'float','float','float']
data = np.genfromtxt('cdc1.dat', dtype=zip(names,types), delimiter=',')

names=['state','j1pop', 'pop']
types=['|S20', 'int','int']
statedat=np.genfromtxt('statepop.dat', dtype=zip(names,types), delimiter=',')

data['homicides'] = data['homicides']/statedat['pop'].astype('float')*1e5
bothk = data['gun_rate'] + data['auto_rate']
data = nprf.append_fields(data,['both'],[bothk], usemask=False, asrecarray=True)

goodstates = np.where(data['state'] != data['state'][8]) #clip DC off

to_plot = ['gun_rate', 'auto_rate', 'homicides','both']
titles = ['Gun Deaths', 'Auto Deaths', 'Gun Homicides', 'All Gun+Auto Deaths']
for thing,title in zip(to_plot,titles):
    # Lambert Conformal map of lower 48 states.
    fig=plt.figure()
    m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,
            projection='lcc',lat_1=33,lat_2=45,lon_0=-95)
    # draw state boundaries.
    # data from U.S Census Bureau
    # http://www.census.gov/geo/www/cob/st2000.html
    shp_info = m.readshapefile('st99_d00','states',drawbounds=True)

    # choose a color for each state based on population density.
    colors={}
    statenames=[]
    cmap = plt.cm.hot_r#gist_rainbow #
    vmin = np.min(data[thing][goodstates]); vmax = np.max(data[thing][goodstates]) # set range.
    #print(m.states_info[0].keys())
    for shapedict in m.states_info:
        statename = shapedict['NAME']
        # skip DC and Puerto Rico.
        if statename not in ['District of Columbia','Puerto Rico']:
            good = np.where(data['state'] == statename)
            pop = data[thing][good][0]
            # calling colormap with value between 0 and 1 returns
            # rgba value.  Invert color range (hot colors are high
            # population), take sqrt root to spread out colors more.
            colors[statename] = cmap((pop-vmin)/(vmax-vmin))[:3]
        statenames.append(statename)
    # cycle through state names, color each one.
    ax = plt.gca() # get current axes instance
    for nshape,seg in enumerate(m.states):
        # skip DC and Puerto Rico.
        if statenames[nshape] not in ['District of Columbia','Puerto Rico']:
            color = rgb2hex(colors[statenames[nshape]]) 
            poly = Polygon(seg,facecolor=color,edgecolor=color)
            ax.add_patch(poly)
    # draw meridians and parallels.
    #m.drawparallels(np.arange(25,65,20),labels=[1,0,0,0])
    #m.drawmeridians(np.arange(-120,-40,20),labels=[0,0,0,1])
    plt.title(title)
    ax1 = fig.add_axes([0.12, 0.08, 0.77, 0.08])
    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)

    cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=cmap,
                                       norm=norm,
                                       orientation='horizontal')
    cb1.set_label('Deaths per 100,000 people')


    plt.savefig(thing+'.png')
