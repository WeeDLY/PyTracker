import psutil
import time, datetime, threading
import pymysql
import datetime
from enum import Enum

from settings import timeInterval, useRuntime, database, logRuntimeInterval
import db, pc, query
import net_cap, cpu_cap
from logger import Log, LogLevel

start_time = time.time()

class CurrentPC():
	def __init__(self):
		self.PCName = pc.GetPCName()
		self.OS = pc.GetOS()
		self.PCBit = pc.GetBit()
		self.CPU = pc.GetCPU()
		self.Mac = pc.GetMac()
		self.TableNet = '%s%dnet' % (self.PCName, self.Mac)
		self.TableCPU = '%s%dcpu' % (self.PCName, self.Mac)

def Startup():
	""" Get information about the current PC """
	currentPC = CurrentPC()

	""" Check if database is set up correct """
	if db.CheckDatabaseSetup(currentPC) is False:
		Log(LogLevel.ERROR, 'Database "%s" is not set up correctly, exiting.' % database)
		return
	else:
		Log(LogLevel.INFO, 'Database: "%s" is set up correctly' % database)

	""" Get the currentPC ID from the DB """
	currentPC.ID = db.ExecuteQueryGet(query.GetID(currentPC))
	if currentPC.ID is None:
		Log(LogLevel.ERROR, 'Could not fetch ID from the database on pc: %s, exiting' % currentPC.PCName)
		return

	Log(LogLevel.INFO, 'Starting capture on PC: %s' % currentPC.PCName)

	net_cap.StartNetworkCapture(currentPC)
	cpu_cap.StartCPUCapture(currentPC)
	GetRuntime(currentPC)

def GetRuntime(currentPC):
	total_runtime = db.ExecuteQueryGet(query.GetRuntime(currentPC.ID))
	total_runtime = total_runtime.seconds
	last_update = 0
	while useRuntime:
		time.sleep(timeInterval)
		total_runtime += timeInterval
		m, s = divmod(total_runtime, 60)
		h, m = divmod(m, 60)
		tid = "%02d:%02d:%02d" % (h, m, s)

		if last_update + logRuntimeInterval <= total_runtime:
			last_update = total_runtime
			Log(LogLevel.INFO, 'Current runtime: %s' % tid)

		db.ExecuteQuery(query.UpdateRuntime(currentPC, tid))

if __name__ == '__main__':
	Startup()
