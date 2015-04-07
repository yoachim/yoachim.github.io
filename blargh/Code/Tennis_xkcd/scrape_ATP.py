# Pull all the available rankings and find the names for any player that has ever been #1

import numpy as np
import urllib2
import re
import time


names = ['n1','n2']
types = ['|S12','|S10']

data = np.genfromtxt('n1_names.dat', dtype=zip(names,types), delimiter=' ')
#fix the 'Juan Carlos underscore
for i,name in enumerate(data['n1']):
    data['n1'][i] = name.replace('_',' ')

names=[]
for i in np.arange(data.size):
    names.append(data['n2'][i]+',&nbsp;'+data['n1'][i])
                 
    
dates = np.genfromtxt('ranking_dates.dat', dtype='|S10')

#temp trim down
#dates = dates[0:20]

results = np.zeros( (dates.size, data.size), dtype=int)
pnames = ['first','second']
ptypes=[int,int]
points = np.zeros( dates.size, dtype = zip(pnames,ptypes))


for i,date in enumerate(dates):
    # Pull the data
    time.sleep(1)
    page = urllib2.urlopen('http://www.atpworldtour.com/Rankings/Singles.aspx?d='+date+'&r=1&c=#').read()
    spot = page.find('"rank">1')
    if spot != -1:
        sub_page = page[spot:spot+400].replace("\n","")
        sub_page = re.sub('.*t=rb">','',sub_page)
        sub_page = re.sub('</a.*','',sub_page).replace(',','')
        try:
            points['first'][i] = int(sub_page)
        except:
            print i
            print sub_page
            import pdb ; pdb.set_trace()
      
    spot = page.find('"rank">2')
    if spot != -1:
        sub_page = page[spot:spot+400].replace("\n","")
        sub_page = re.sub('.*t=rb">','',sub_page)
        sub_page = re.sub('</a.*','',sub_page).replace(',','')
        try:
            points['second'][i] = int(sub_page)
        except:
            print i
            print sub_page
            import pdb ; pdb.set_trace()
    for j,name in enumerate(names):
        if name in page:
            #find the location of the name
            spot = page.find(name)
            #pull the ranking out
            sub_page = page[spot-200:spot].replace("\n","")
            sub_page = re.sub('.*rank">','',sub_page)
            sub_page = re.sub('<.*','',sub_page)
            ranking = int(sub_page)
            results[i][j] = ranking

np.savez('mens_rankings.npz', results=results, names=names, dates=dates, points=points)
