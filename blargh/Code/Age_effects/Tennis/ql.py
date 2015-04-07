import numpy as np

dat = np.loadtxt('USA_girls_trimmed.dat', dtype=[('day','int'),('month','S10'),('year', 'int')])

months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
mo_num = np.arange(12)

mo_dist = dat['day']*0-666

for i in np.arange(np.size(months)):
    good = np.where(dat['month'] == months[i])
    mo_dist[good] = mo_dist[good]*0+i

hist(mo_dist, bins=12)
