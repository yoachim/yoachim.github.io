from bs4 import BeautifulSoup
import re


# Need to wget all the years I want.

def read_win_loss(filename):
    filename = 'uw/1950-schedule.html'
    with open(filename, 'r', encoding='utf-8') as tempfile:
        data = tempfile.read()
    indx = [m.start() for m in re.finditer('game_result', data)]
    