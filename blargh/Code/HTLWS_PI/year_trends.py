import numpy as np
import pylab as pyl

names=['year', 'deaths', 'pop', 'rate']
types=['int','int', 'int', 'float']
hom = np.genfromtxt('cdc_firearm_homicide.dat', dtype=zip(names,types))


fire= np.genfromtxt('cdc_firearmdeaths.dat', dtype=zip(names,types))


#plot(fire['year'],fire['rate']- hom['rate'])

names=['year', 'rate']
types=['int','float']
auto = np.genfromtxt('auto_history.dat', dtype=zip(names,types), usecols=(0,5))



plot(hom['year'], hom['rate'], 'r', label='Gun Homicides', linewidth=2)
plot(fire['year'],fire['rate'], 'b', label='Gun Deaths', linewidth=2)
plot(auto['year'],auto['rate'], 'g', label='Auto Deaths', linewidth=2)

xlim([1980,2011])
ylim([0,25])
legend()

xlabel('Year')
ylabel('Deaths per 100,000 people')

savefig('dpery.png')

figure()
plot(hom['year'], hom['rate'], 'r', linewidth=2, label='Gun Homicides')
title('Gun Homicides')
xlabel('Year')
ylabel('Deaths per 100,000 people')
savefig('ghompy.png')
