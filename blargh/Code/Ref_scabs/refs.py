
#replacement refs were 31-17

#play 10,000 seasons of football with 48 games each
hg = np.random.rand(10000,48) 
#home team wins 56% of the time
hg[np.where(hg <= 0.56)]=1 
#the rest are losses
hg[np.where(hg < 1)]=0 
#total up the wins per season
ack = np.sum(hg, axis=1) 
print 'probability of home team winning 31 or more games with 1999-2008 refs = %.2f'%(np.size(np.where(ack >= 31)) /10000.*100)+'%' 

print 'percent of sims farther from the expected value than the replacements =%.2f'%(np.size(np.where(np.abs(ack-26.88) >= 31-26.88))/10e3*100)


hist(ack,np.arange(50)-.5)
axvline(x=31)

