import numpy as np
from pylab import *
from scipy.stats import kstest,uniform
from numpy.lib.recfunctions import append_fields

def halfBias(dist):
    """Calculate how many additional elements are in the 1st half of the range """
    mp = (np.max(dist)-np.min(dist))/2.
    first_half = np.size(np.where(dist < mp))*1.
    bias = first_half/np.size(dist)
    return bias

nba = np.genfromtxt('NBA/player_ages_trimmed.dat', dtype=[('name','S20'),('month','S3'),('day','uint')])

months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
months_num = np.arange(12)+1
days = np.array([31,28,31,30,31,30,31,31,30,31,30,31])
days_cum = days*0.
for i in np.arange(days.size-1)+1: days_cum[i] = np.sum(days[:i])
month_num = np.zeros(np.size(nba))
month_date = np.zeros(np.size(nba))

for i in np.arange(np.size(months)):
    good = np.where(nba['month'] == months[i])
    month_num[good] = days_cum[i]
    month_date[good] = months_num[i]

nba_days = month_num+nba['day']
nba = append_fields(nba,'cudays', nba_days, 'float', usemask=False)


nhl =  np.genfromtxt('NHL/player_ages_trimmed.dat', dtype=[('year','int'),('month','int'),('day','uint')])

month_days = np.zeros(nhl.size,dtype=float)
for i in np.arange(np.size(months)):
    good = np.where(nhl['month'] == i+1)
    month_days[good] = days_cum[i]
                   
nhl_days = month_days + nhl['day']

nhl = append_fields(nhl,'cudays', nhl_days, 'float', usemask=False)


nfl = np.loadtxt('NFL/player_ages_trimmed.dat', dtype=[('month','S10'),('day','int'),('year', 'int')])

months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
mo_num = np.arange(12)

mo_dist = nfl['day']*0-666
month_days = np.zeros(nfl.size,dtype=float)
for i in np.arange(np.size(months)):
    good = np.where(nfl['month'] == months[i])
    mo_dist[good] = mo_dist[good]*0+i
    month_days[good] = days_cum[i]

nfl_days = month_days + nfl['day']

nfl = append_fields(nfl, 'cudays', nfl_days, 'float', usemask=False)



btennis = np.loadtxt('Tennis/USA_boys_trimmed.dat', dtype=[('day','int'),('month','S10'),('year', 'int')])
mo_dist = btennis['day']*0-666
month_days = np.zeros(btennis.size,dtype=float)

for i in np.arange(np.size(months)):
    good = np.where(btennis['month'] == months[i])
    mo_dist[good] = mo_dist[good]*0+i
    month_days[good] = days_cum[i]

bdays = month_days+ btennis['day']
btennis = append_fields(btennis, 'cudays', bdays, 'float', usemask=False)


gtennis = np.loadtxt('Tennis/USA_girls_trimmed.dat', dtype=[('day','int'),('month','S10'),('year', 'int')])
mo_dist = gtennis['day']*0-666
month_days = np.zeros(gtennis.size,dtype=float)

for i in np.arange(np.size(months)):
    good = np.where(gtennis['month'] == months[i])
    mo_dist[good] = mo_dist[good]*0+i
    month_days[good] = days_cum[i]

bdays = month_days+ gtennis['day']
gtennis = append_fields(gtennis, 'cudays', bdays, 'float', usemask=False)






expected_dist = uniform(loc=1,scale=365)


sports = [nba,nfl,nhl,btennis,gtennis]
lables=['NBA', 'NFL','NHL', 'Boys Tennis', 'Girls Tennis']
fns = ['nba','nfl','nhl','bt','gt']

for i in range(len(sports)):
    ks = kstest(sports[i]['cudays'], expected_dist.cdf)
    figure()
    hist(sports[i]['cudays'], bins=12)
    title(lables[i])
    xlabel('Days')
    ylabel('#')
    axhline(np.size(sports[i]['cudays'])/12., color='k')
    if ks[1] < .05:
        col = 'r'
    else:
        col = 'k'
    text(.85,.85,'p=%.3g'%ks[1], color=col, transform = gca().transAxes)
    savefig(fns[i]+'.png', format='png')





qbs = np.genfromtxt('NFL/qb_ages.dat', dtype=[('month','S10'),('day','int'),('year','int')])
qb_days = qbs['day']*0.
for month,days in zip(months,days_cum):
    good = np.where(qbs['month'] == month)
    qb_days[good] = qb_days[good]+days

qb_days = qb_days+qbs['day']


ack = kstest(qb_days, expected_dist.cdf)




ack = kstest(nhl_days, expected_dist.cdf)










#well, I guess I want to look at MLB, NFL, and Tennis as well.  Curious when the trend gets set.  If it happens in tennis, it might mean that its a really quick effect (like the younger kids quit fast, or the older kids get commited fast).
