import numpy as np
import subprocess
from pylab import *

np.random.seed(seed=42)

#O can use np.tile to make a large array

#read in season, name, birth year, death year, gender

#want array that is n_names x nseasons long
# ages = np.arange(n_seasons)+1989-birth_year


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

def pull_dates(url):
    subprocess.Popen('wget %s -O temp.html'%url, shell=True).wait()
    bday=subprocess.Popen('''grep 'class="bday'  temp.html''', shell=True, stdout=subprocess.PIPE).stdout.readlines()
    if len(bday) == 0:
        position = -1
    else:
        #position = bday[0].find('-')
        position = bday[0].find('"bday">')
    if position != -1:
        #bday = np.float(bday[0][position-4:position])
        bday = np.float(bday[0][position+7:position+11])
    else:
        bday = -1
    dday=subprocess.Popen('''grep 'class="dday'  temp.html''', stdout=subprocess.PIPE, shell=True).stdout.readlines()
    if len(dday) == 0:
        position = -1
    else:
        dday[0]=dday[0].replace('deathdate','')
        dday[0]=dday[0].replace(' ','')
        position = dday[0].find('"dday">')
    if position != -1:
        dday = np.float(dday[0][position+7:position+11])
    else:
        dday = -1
    return bday,dday


#use wget to grab a file, grep to find bday,
#read the string in and use .find('-') to grab the birth year

#subprocess.Popen('ls', stdout=subprocess.PIPE).stdout.readlines()

#I can replicate things with np.tile.  eg, result = np.random.rand(1e5,n_names,nseasons) - np.tile(1e5,actuary_prob)

def find_dates():
    data = np.genfromtxt('simpsons.cvs', delimiter=',,', dtype=[('season','<i8'), ('Guest_star', '|S40'), ('URL','|S100')], skip_header=1)

    #need to do a unique on the names
    data.sort(order=['URL','season'])
    temp, ind = np.unique(data['URL'], return_index=True)
    data=data[ind]
    data.sort(order='season')
    #data2={}
    #data2['bday'] = np.zeros(np.float(np.size(ind)))
    #data2['dday'] = np.zeros(np.float(np.size(ind)))
    file = open('wdates.dat','w')
    print >>file, 'season,, Guest_star,,  bday,, dday,, url'
    for i in np.arange(np.size(data)):
        bday, dday = pull_dates(data['URL'][i])
        print >>file, "%i,,%s,,%d,,%d,,%s"%(data['season'][i],data['Guest_star'][i],bday,dday, data['URL'][i])

    file.close()


def plot_simp(gender='M'):

    data = np.genfromtxt('wdates.dat', delimiter=',,', dtype=[('season','<i8'), ('Guest_star', '|S40'), ('bday','float'),('dday','float'),('URL','|S100')], skip_header=1)

    #note, the movie was in 2007.  Season 1 was December 17, 1989.  Prob just call that 1990.

    data = data[np.where(data['bday'] != -1)]

    beatles = np.where( (data['Guest_star'] == 'Ringo Starr') | (data['Guest_star'] == 'George Harrison') | (data['Guest_star'] == 'Paul McCartney'))

    print 'number of celebrities = %i'%np.size(data['bday'])
    print 'number that have died = %i'%np.size(np.where(data['dday'] != -1))

    figure()
    good = np.where(data['dday'] != -1)
    ord = np.argsort(data['dday'][good])
    cuum=np.arange(np.size(good))
    uy = np.unique(data['dday'][good][ord])
    ack = np.searchsorted(data['dday'][good][ord],uy,side='right')-1
    plot(data['dday'][good][ord][ack],cuum[ack], 'k',linewidth=2, label='Observed')
    ylabel('Cumulative Dead Guests')
    xlabel('Year')
    title('Curse of the Simpsons!')
    legend(loc=2)
    savefig('curse1'+gender+'.png',type='png')

    #clf()
    #bins=np.arange(2013-1996)+1996.5
    #bins=np.arange(2015-1996)+1996.5
    #hist(data['dday'][good], bins)
    #xlabel('year')
    #ylabel('# of deaths')

    #originally aired Dec 1989.  Let's just call 1990 the 1st season
    years = data['season']+1989.
    years[np.where(data['season'] == -1)] = 2007
    u_years = np.unique(years)
    #u_years= np.append(u_years, [2014,2015])

    #now I want an array with the ages of each guest
    prob_array = np.zeros((np.size(years), np.size(u_years)), dtype='float')
    #mask_array = age_array*0
    ny = np.size(u_years)
    ng = np.size(data)

    for i in np.arange(np.size(years)):
        age = np.arange(ny)+1989 - data['bday'][i]
        prob_array[i,:] = actuary_prob(age,gender) #probability of dying in a given year
        prob_array[i,:][np.where(u_years <= years[i])] = 0 #Have to live long enogh to make it on the show



    n_run = 1e3
    results = np.zeros((ny,n_run))
    nb = np.zeros(n_run)
    LN = np.where(data['Guest_star'] == 'Leonard Nimoy')
    nLN = np.zeros(n_run)

    for i in np.arange(n_run):
        draw = np.random.rand(ng,ny)
        resid = prob_array - draw
        live = np.where(resid < 0)
        dead = np.where(resid > 0)
        draw[dead] = 0
        draw[live] = 1
        for j in np.arange(ny-1)+1:
            draw[:,j] = draw[:,j]*draw[:,j-1]
        draw = np.abs(draw-1) #now dead = 1
        #print draw.shape, draw[:,-1].shape
        nb[i] = np.sum(draw[:,-1][beatles])
        nLN[i] = np.sum(draw[:,-1][LN])
        results[:,i] = np.sum(draw,axis=0)

    #import pdb ; pdb.set_trace()

    figure()
    plot(data['dday'][good][ord][ack],cuum[ack], 'k',linewidth=2, label='Observed')
    ylabel('Cumulative Dead Guests')
    xlabel('Year')
    title('Curse of the Simpsons!')

    plot(u_years,np.mean(results,axis=1), 'b' , label='Simulated')
    plot(u_years, np.percentile(results,1,axis=1),'b--', label='99,1 Percentile')
    plot(u_years, np.percentile(results,99,axis=1),'b--')
    legend(loc=2)

    print 'Dead %s expected = %i'%(gender,np.max(np.mean(results,axis=1)))

    savefig('curse2'+gender+'.png',type='png')

    figure()
    plot(data['dday'][good][ord][ack],cuum[ack], 'k',linewidth=2)
    ylabel('Cumulative Dead Guests')
    xlabel('Year')
    title('Curse of the Simpsons!')
    plot(u_years,np.mean(results,axis=1), 'b', label='Simulated')
    plot(u_years, np.percentile(results,1,axis=1),'b--', label='99,1 Percentile')
    plot(u_years, np.percentile(results,99,axis=1),'b--')
    plot(u_years+3,np.mean(results,axis=1), 'g', label='Simulated + 3 yr')
    legend(loc=2)
    savefig('curse3'+gender+'.png',type='png')

    for i in np.arange(4):
        print 'number of times there are %i dead beatles = %i'%(i,np.size(np.where(nb == i)))


    #just make a simple histogram
    figure()
    good = np.where(data['dday'] != -1)
    hist(data['dday'][good]-data['bday'][good])
    xlabel('Age (years)')
    ylabel('# of deaths')
    text(30,14,'mean = %2.1f yr'% np.mean(data['dday'][good]-data['bday'][good]))
    text(30,13,'median = %2.1f yr'% np.median(data['dday'][good]-data['bday'][good]))

    print 'median death age = %f, mean death age = %f'%(np.median(data['dday'][good]-data['bday'][good]), np.mean(data['dday'][good]-data['bday'][good]))
    savefig('curse_hist.png', type='png')


#wow, so given how old the celebrities were when they first appeared, we would actually expect MORE dead celebs.  But if I use the female actuarial table, it looks like a great match!  Could it be that being a rich celebrity gives you the same health benefits as being female?


#Need to double check more of the entries that have -1 for bday!

plot_simp()
plot_simp(gender='F')
