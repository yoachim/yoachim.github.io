
import numpy as np
import subprocess
from pylab import *

def actuary_prob(years, gender):
    result = years*0.
    #read in the table
    if not hasattr(actuary_prob, 'table'):
        print 'reading table'
        actuary_prob.table=table=np.genfromtxt('actuary_table.dat', names=True)
    table=actuary_prob.table
    uyears = np.unique(years)
    for i in uyears:
        good=np.where( (years == i) & (gender == 'M') )
        result[good] = table['male_prob'][np.where(table['age'] == i)]
    for i in uyears:
        good=np.where( (years == i) & (gender == 'F') )
        result[good] = table['female_prob'][np.where(table['age'] == i)]
    return result

data = np.genfromtxt('wdates.dat', delimiter=',,', dtype=[('season','<i8'), ('Guest_star', '|S40'), ('bday','float'),('dday','float'),('URL','|S100')], skip_header=1)

    #note, the movie was in 2007.  Season 1 was December 17, 1989.  Prob just call that 1990.

data = data[np.where(data['bday'] != -1)]

beatles = np.where( (data['Guest_star'] == 'Ringo Starr') | (data['Guest_star'] == 'George Harrison') | (data['Guest_star'] == 'Paul McCartney'))

bday = np.mean(data['bday'][beatles])
season = np.mean(data['season'][beatles])

years = np.arange(2013-1989)+(1989-bday)
probs = actuary_prob(np.round(years),'M')
live_prob = 1-probs
live_prob=live_prob.prod()

print 'Prob 3 live = %f'%live_prob**3
print 'Prob 2 live = %f'%(3.*(live_prob**2-live_prob**3))
print 'Prob 1 live = %f'%(3.*(live_prob)*(1.-live_prob)**2)
print 'Prob 0 live = %f'%((1.-live_prob)**3)
