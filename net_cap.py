import psutil
import datetime, time, threading
import db, pc, query, settings
from logger import Log, LogLevel
from enum import Enum

class interface(Enum):
    eth0 = 'eth0'
    wlan0 = 'wlan0'
    lo = 'lo'
    pp0 = 'pp0'
    notSet = 'all'

class NetworkSession():
	def __init__(self):
		self.startDate = str(datetime.datetime.now().strftime("%Y%m%d"))
		self.startTime = datetime.datetime.now().strftime("%H%M%S")

		self.interface = interface.notSet
		self.bytes_sent = 0
		self.bytes_recv = 0
		self.packets_sent = 0
		self.packets_recv = 0
		self.errin = 0 # Errors while recv
		self.errout = 0 # Errors while sent
		self.dropin = 0 # Dropped packets incoming
		self.dropout = 0 # Dropped packets outgoing

	def SetSession(self):
		if self.interface is not interface.notSet:
			network = psutil.net_io_counters(pernic=True)
			self.bytes_sent = network[self.interface.name].bytes_sent
			self.bytes_recv = network[self.interface.name].bytes_recv
			self.packets_sent = network[self.interface.name].packets_sent
			self.packets_recv = network[self.interface.name].packets_recv
			self.errin = network[self.interface.name].errin
			self.errout = network[self.interface.name].errout
			self.dropin = network[self.interface.name].dropin
			self.dropout = network[self.interface.name].dropout
		else:
			network = psutil.net_io_counters()
			self.bytes_sent = network[0]
			self.bytes_recv = network[1]
			self.packets_sent = network[2]
			self.packets_recv = network[3]
			self.errin = network[4]
			self.errout = network[5]
			self.dropin = network[6]
			self.dropout = network[7]

	def SetInterface(self, interface):
		try:
			self.interface = interface
		except:
			Log(LogLevel.WARNING, 'Can not set interface to %s' % interface)

def GetSessionValue(firstSession, lastSession):
	session = NetworkSession()
	session.bytes_sent = lastSession.bytes_sent - firstSession.bytes_sent
	session.bytes_recv = lastSession.bytes_recv - firstSession.bytes_recv
	session.packets_sent = lastSession.packets_sent - firstSession.packets_sent
	session.packets_recv = lastSession.packets_recv - firstSession.packets_recv
	session.errin = lastSession.errin - firstSession.errin
	session.errout = lastSession.errout - firstSession.errout
	session.dropin = lastSession.dropin - firstSession.dropin
	session.dropout = lastSession.dropout - firstSession.dropout
	return session

def NetworkCapture(currentPC, interface):
	while settings.useNetCapture:
		sessionStart = NetworkSession()
		sessionStart.SetInterface(interface)
		sessionStart.SetSession()

		time.sleep(settings.netInterval)

		sessionCapture = NetworkSession()
		sessionCapture.SetInterface(sessionStart.interface)
		sessionCapture.SetSession()
		sessionCapture = GetSessionValue(sessionStart, sessionCapture)

		db.ExecuteQuery(query.InsertNetTable(currentPC, sessionStart, sessionCapture))
		Log(LogLevel.INFO, 'Inserted NetSession to the database')

def StartNetworkCapture(currentPC):
	interfaces = pc.GetInterface()
	if len(interfaces) <= 0:
		Log(LogLevel.WARNING, 'No network interface is in use to capture on, exiting thread')
		return

	for i in interfaces:
		captureInterface = True
		for disallow_interface in settings.disallowInterface:
			if i is disallow_interface:
				Log(LogLevel.WARNING, 'Interface: %s, is disabled for network capture.' % i.name)
				captureInterface = False
		if captureInterface:
			Log(LogLevel.INFO, 'Starting Network capture on interface: %s' % i)
			net_thread = threading.Thread(target=NetworkCapture, args=(currentPC, i))
			net_thread.daemon = True
			net_thread.start()
