
file = open('pull.sh', 'w')
for year in range(1900,2017):
    file.write('wget https://www.sports-reference.com/cfb/schools/washington/%i-schedule.html' % year)
    file.write(' \n')
file.close()

