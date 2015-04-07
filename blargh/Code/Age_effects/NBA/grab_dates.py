import subprocess

outfile = open('player_ages.dat','w')

#file = open('playerfile.html','r')
lines = [line.strip() for line in open('playerfile.html')]
bday = []

for line in lines:
    subprocess.Popen('wget http://www.nba.com%s -O temp.html'%line, shell=True).wait()
    born=subprocess.Popen('''awk '/Born/{getline; print}'  temp.html''', shell=True, stdout=subprocess.PIPE).stdout.readlines()[0].strip()
    bday.append(born)
    print >>outfile, '%s   %s'%(line,born)

outfile.close()

