import pymysql

def solutionLookup(problem):
	conn = pymysql.connect(db='resume_database', user='admin', passwd='', host='127.0.0.1')
	with conn.cursor() as cur:
		cur.execute("SELECT solution FROM puzzle_solutions WHERE problem = '%s'" % problem)
		for row in cur:
			return row[0]
