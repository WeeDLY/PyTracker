import pymysql
import platform
import pc, query
from logger import Log, LogLevel
import settings

def CheckServerConnection():
	try:
		conn = pymysql.connect(user=settings.username, passwd=settings.password, host=settings.server)
		return True
	except:
		return False

def CheckDatabaseConnection():
	try:
		conn = pymysql.connect(user=settings.username, passwd=settings.password, host=settings.server, database=settings.database)
		return True
	except:
		return False

def ExecuteQueryServer(query):
	try:
		conn = pymysql.connect(user=settings.username, passwd=settings.password, host=settings.server)
		cur = conn.cursor()
		cur.execute(query)
		return True
	except:
		return False

def ExecuteQuery(query):
	try:
		conn = pymysql.connect(user=settings.username, passwd=settings.password, host=settings.server, database=settings.database, autocommit=True)
		cur = conn.cursor()
		cur.execute(query)
		return True
	except Exception as e:
		Log(LogLevel.WARNING, 'ExecuteQuery: %s\nOn query: %s' % (e, query))
		return False

def ExecuteQueryGet(query):
	try:
		conn = pymysql.connect(user=settings.username, passwd=settings.password, host=settings.server, database=settings.database)
		cur = conn.cursor()
		cur.execute(query)
		return cur.fetchone()[0]
	except Exception as e:
		Log(LogLevel.WARNING, 'ExecuteQueryGet: %s\nOn query: %s' % (e, query))
		return False

""" Checks if the database is set up correctly, this includes tables for the currentPC aswell """
def CheckDatabaseSetup(currentPC):
	retry = 5 + 1
	retryBreak = retry - 2

	for i in range(1, retry):
		if(CheckServerConnection()):
			break
		else:
			Log(LogLevel.WARNING, 'Not able to get a server connection. Try #%d' % i)
		if i > retryBreak:
			Log(LogLevel.ERROR, 'Not able to get a server connection. Exiting.')
			return False

	for i in range(1, retry):
		if(CheckDatabaseConnection()):
			break
		else:
			ExecuteQueryServer(query.CreateDatabase())
			Log(LogLevel.WARNING, 'Not able to get a database connection. Try #%d' % i)
		if i > retryBreak:
			Log(LogLevel.ERROR, 'Not able to get a database connection. Exiting.')
			return False
	for i in range(1, retry):
		if(CheckTable(settings.mainTable)):
			break
		else:
			ExecuteQuery(query.CreateMainTable())
			Log(LogLevel.WARNING, 'Not able to create main table: %s. Try #%d' % (settings.mainTable, i))
		if i > retryBreak:
			Log(LogLevel.ERROR, 'Not able to create main table. Exiting.')
			return False

	# Checking Table for the net statistics
	for i in range(1, retry):
		if(CheckTable(currentPC.TableNet)):
			break
		else:
			ExecuteQuery(query.InsertMainTable(currentPC))
			ExecuteQuery(query.CreateTableNet(currentPC.TableNet))
			Log(LogLevel.WARNING, 'Not able to create table to store network statistics. Try #%d' % i)
		if i > retryBreak:
			Log(LogLevel.ERROR, 'Not able to create table to store network statistics. Exiting.')
			return False

	# Checking Table for the cpu statistics
	for i in range(1, retry):
		if(CheckTable(currentPC.TableCPU)):
			break
		else:
			ExecuteQuery(query.CreateTableCPU(currentPC.TableCPU))
			Log(LogLevel.WARNING, 'Not able to create table to store CPU statistics. Try #%d' % i)
		if i > retryBreak:
			Log(LogLevel.ERROR, 'Not able to create table to store CPU statistics. Exiting.')
			return False

def CheckTable(table):
	return TableExists(table)

def TableExists(table):
	try:
		conn = pymysql.connect(user=settings.username, passwd=settings.password, host=settings.server, database=settings.database)
		cur = conn.cursor()
		sql = query.TableExists(table)
		cur.execute(sql)
		if cur.fetchone():
			return True
		else:
			return False
	except Exception as e:
		return False
