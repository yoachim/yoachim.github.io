import numpy as np
import matplotlib.pylab as plt
import datetime

names=['loc', 'bm','bd','by', 'dm', 'dd', 'dy', 'rm', 'rd', 'ry']
types = ['|S15']
types.extend([int]*9)

data = np.genfromtxt('travel.dat', dtype = zip(names, types))

bookDates = np.array([datetime.date(d['by'], d['bm'], d['bd']).toordinal() for d in data])
returnDates = np.array([datetime.date(d['ry'], d['rm'], d['rd']).toordinal() for d in data])

md = bookDates.min()

bookDates = bookDates - md
returnDates = returnDates - md

booked = np.zeros(returnDates.max()+1)

for day in bookDates:
    booked[day:] = booked[day:]+1

for day in returnDates:
    booked[day:] = booked[day:] -1


# say I always have 3 mo warning (otherwise I get a lot of gaps that aren't true)
trips = np.zeros(returnDates.max()+1)
for day in returnDates:
    minDay = day-150
    if minDay < 0:
        minDay = 0
    trips[minDay:day] = trips[minDay:day]+1

#plt.plot(booked)
plt.plot(np.arange(trips.size)/365.25, trips)
plt.xlabel('Years Since Moving')
plt.ylabel('Number of Trips Booked')

plt.show()
