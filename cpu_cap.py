import psutil
import datetime, time, threading
import db, query
from settings import useCPUCapture, cpuInterval
from logger import Log, LogLevel

class CPUSession():
	def __init__(self):
		self.date = str(datetime.datetime.now().strftime("%Y%m%d"))
		self.time = datetime.datetime.now().strftime("%H%M%S")
		vir_mem = psutil.virtual_memory()
		self.total = vir_mem[0]
		self.available = vir_mem[1]
		self.percent = vir_mem[2]
		self.used = vir_mem[3]

def CPUCapture(currentPC):
	while useCPUCapture:
		cpuSession = CPUSession()

		time.sleep(cpuInterval)

		Log(LogLevel.INFO, 'Inserting CPU statistics to the database')
		db.ExecuteQuery(query.InsertCPUTable(currentPC, cpuSession))

def StartCPUCapture(currentPC):
	Log(LogLevel.INFO, 'Starting CPU capture on PC: %s' % currentPC.PCName)
	cpu_thread = threading.Thread(target=CPUCapture, args=(currentPC,))
	cpu_thread.daemon = True
	cpu_thread.start()
