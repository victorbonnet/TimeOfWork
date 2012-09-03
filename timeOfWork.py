import datetime
import time
import signal
import sys
import sqlite3

conn = sqlite3.connect('work.db')
company = "victor"

def initDB():
	c = conn.cursor()
	c.execute("create table if not exists  Session(company TEXT, start INT, end INT, time FLOAT)")
	conn.commit()
	c.close()

def startWork():
	global startDate, endDate;
	startDate = datetime.datetime.today()

def stopWork():
	global startDate, endDate;
        endDate = datetime.datetime.today()
        timeOfWork = endDate - startDate
        print "Time of Work: %s" % str(timeOfWork)
	cur = conn.cursor()    
	cur.execute("insert into Session VALUES (?, ?, ?, ?)",(company, time.mktime(startDate.timetuple()), time.mktime(endDate.timetuple()), timeOfWork.total_seconds()))
	conn.commit()
        cur.close()

def displayStats():
	cur = conn.cursor()
	list = []
	for row in cur.execute('SELECT start, end, time FROM Session WHERE company = ? ORDER BY start', [company]):
        	list.append(row[2])
		print "start: ", datetime.datetime.fromtimestamp(int(row[0])).strftime('%Y-%m-%d %H:%M:%S'), ", end: ", datetime.datetime.fromtimestamp(int(row[1])).strftime('%Y-%m-%d %H:%M:%S'), ", time: ", str(row[2])
	cur.close()

	total = 0
	for x in list:
		total += x
	print "work time:", total//3600, "hours"
	print "work time:", total//60, "minutes"
	print "work time:", total, "seconds"

if __name__=="__main__":
	initDB()
	if len(sys.argv) < 2:
		print "start|stats"
                sys.exit(0)
	elif (sys.argv[1] == "start"):
		if len(sys.argv) < 3:
			print "The company name is require"
			sys.exit(0)
		else:
			company = sys.argv[2]
			startWork()
	elif (sys.argv[1] == "stats"):
		if len(sys.argv) < 3:
                        print "The company name is require"
                        sys.exit(0)
                else:
                        company = sys.argv[2]
			displayStats()
			sys.exit(0)
	else:
		print "start|stats"
		sys.exit(0)

def signal_handler(signal, frame):
        stopWork()
	sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)
signal.pause()
