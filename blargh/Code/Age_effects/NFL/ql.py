import numpy as np
from scipy.stats import kstest,uniform

dat = np.loadtxt('kp_ages.dat', dtype=[('month','S10'),('day','int'),('year', 'int')])

months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
mo_num = np.arange(12)

mo_dist = dat['day']*0-666

for i in np.arange(np.size(months)):
    good = np.where(dat['month'] == months[i])
    mo_dist[good] = mo_dist[good]*0+i

hist(mo_dist, bins=12)
expected_dist = uniform(loc=1,scale=12)

ack = kstest(mo_dist, expected_dist.cdf)
