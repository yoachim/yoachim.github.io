import numpy as np

dat = np.genfromtxt('player_ages_trimmed.dat', dtype=[('year','int'),('month','int'),('day','uint')])

#months=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
months = np.arange(12)

days = np.array([31,28,31,30,31,30,31,31,30,31,30,31])
days_cum = days*0.
for i in np.arange(days.size-1)+1: days_cum[i] = np.sum(days[:i])
month_num = np.zeros(np.size(dat))

for i in np.arange(np.size(months)):
    good = np.where(dat['month'] == months[i])
    month_num[good] = days_cum[i]

daysintoyear = month_num+dat['day']

daysintoyear.sort()
num = np.arange(daysintoyear.size, dtype='float')
num=num/num.max()

plot(daysintoyear,num)
plot([0,365],[0,1])
