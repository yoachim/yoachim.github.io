import subprocess
import time

#outfile = open('player_ages.dat','w')
outfile = open('kp_ages.dat','w')


lines = [line.strip() for line in open('kphtml.dat')]
url_front = 'http://sports.yahoo.com'
bday = []
i=0.
num = len(lines)
for line in lines:
    born = subprocess.Popen('wget -q -O - %s%s | grep Born'%(url_front,line), shell=True, stdout=subprocess.PIPE).stdout.readlines()
    if len(born) != 0:
        born = born[0].strip()
        bday.append(born)
        print >>outfile, born
    i += 1
    time.sleep(.5)
    print i/num*100

outfile.close()

#AAARG, clearly I should just be sending the wget to stdout and pipe it to a grep and then read the result.  duh
#wget -q -O - http://www.example.com/file.html 
