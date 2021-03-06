from datetime import datetime, timedelta
from time import mktime
import json
from random import randint

def main():
    now = datetime.now()
    with open('ph.json', 'w+') as f:
        s = json.dumps([{'time' : int(mktime((now - timedelta(days = i)).timetuple())), 'ph' : 0} for i in range(0, 120)])
        f.write(s)
    with open('temp.json', 'w+') as f:
        s = json.dumps([{'time' : int(mktime((now - timedelta(days = i)).timetuple())), 'temp' : 0} for i in range(0, 120)])
        f.write(s)
    with open('level.json', 'w+') as f:
        s = json.dumps([{'time' : int(mktime((now - timedelta(days = i)).timetuple())), 'level' : 0} for i in range(0, 120)])
        f.write(s)




if __name__ == '__main__':
    main()