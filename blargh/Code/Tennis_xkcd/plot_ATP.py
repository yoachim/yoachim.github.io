# plot up the results of the ATP scrape

import numpy as np
import matplotlib.pylab as plt
import datetime


def plotPlayer(times, ranks, name='Name', norank=0, nweeks = 52,
               height=0.8 , color='gray', retireDate=None):
    """Plot each line segment.  Make it red for #1 times.   Find a long
    flat strech and put name on it.

    assume times are ordered
    demand more than nweeks to be plotted"""
    
    tryplot = 0
    #find when ranked 1
    toprank =np.where((ranks < 2) & (ranks != norank) )[0]
    dateDiff = np.diff(times[toprank])
    if toprank.size > nweeks:
        if retireDate is not None:
            # pad this out in case they won one last tounry (e.g., Pete)
            good = np.where( (ranks != norank) & (times < retireDate+30./365.25) )[0]
        else:
            good = np.where(ranks != norank)[0]
        plt.semilogy(times[good], ranks[good], color)
        if retireDate is not None:
            plt.plot(times[good][-1], ranks[good][-1], '*',color=color, markersize=20)
            print name+' retire rank = %i'%ranks[good][-1]

        
        gappts = np.where(dateDiff > 8/365.25)[0]+1
        gappts = np.insert(gappts, 0, 0)
        gappts = np.append(gappts, toprank.size)

        #for i in np.arange(gappts.size-1):
        #    plt.plot(times[toprank][gappts[i]:gappts[i+1]],
        #             ranks[toprank][gappts[i]:gappts[i+1]], 'r')
        #ax = plt.gca()
        #ax.annotate(name, xy)
        plt.text(times[toprank][0], height , name, color=color, alpha=.4)
        tryplot = 1
    return tryplot



    

mens = np.load('mens_rankings.npz')
rankings = mens['results'].copy()+0.
names = mens['names'].copy()
points = mens['points'].copy()

times = np.zeros(mens['dates'].size, dtype=float)
t0 = datetime.date(1970,1,1)
for i,date in enumerate(mens['dates']):
    stringDate = date.split('.')
    dateobj = datetime.date(int(stringDate[2]),
                            int(stringDate[1]), int(stringDate[0]))
    times[i] = (dateobj-t0).total_seconds()/3600./24/365.25+1970. # in days

plt.xkcd()
fig = plt.figure(figsize=(10,5))

colors = ['green', 'red', 'blue', 'purple', 'orange', 'black']
heights = [0.6,0.9, 0.7, 0.5, .15, .2, 1.8, 0.08, 0.3, 0.4 ]
counter=0

rnames=['n1','n2', 'date']
rtypes=['|S10', '|S10', '|S10']
retireData = np.genfromtxt('last_match.dat', dtype=zip(rnames,rtypes), delimiter=' ')
retireNames =[]
for i in np.arange(retireData.size):
    retireNames.append(retireData['n1'][i] + ' '+retireData['n2'][i])
retireNames = np.array(retireNames)

firstTimeOne = []
for i in  np.arange(names.size):
    good = np.where(rankings[:,i] == 1)[0]
    firstTimeOne.append(np.min(times[good]))
order = np.argsort(firstTimeOne)


# rank fudge
rankFudge = times*0.
good = np.where(points['first'] != 0)[0]
rankFudge[good] = (points['first'][good]+0.)/points['second'][good]

for i in np.arange(times.size):
    if (1. in rankings[i,:]) & (rankFudge[i] != 0):
        top = np.where(rankings[i,:] == 1)
        rankings[i,top] = rankings[i,top]+1-rankFudge[i]


for j in np.arange(names.size):
    i = order[j]
    name = names[i].replace('&nbsp;','').split(',')
    name = name[1]+' '+name[0]
    if name in retireNames:
        rdate = retireData['date'][np.where(retireNames == name)[0]]
        rdate = rdate[0].split('.')
        rdate = datetime.date(int(rdate[2]), int(rdate[1]), int(rdate[0]))
        rdate = (rdate-t0).total_seconds()/3600./24/365.25+1970.
    else:
        rdate = None
    
    tryplot = plotPlayer(times[::-1], rankings[:,i][::-1],
                         name=name,
                         color=colors[counter%len(colors)],
                         height=heights[counter%len(heights)],
                         retireDate=rdate)
    if tryplot != 0:
        counter = counter+1

plt.ylim([100,.05])
plt.ylabel('ATP Rank')
plt.xlabel('Year')
plt.title("Men's Tennis")
plt.savefig('atp_plot.png')
