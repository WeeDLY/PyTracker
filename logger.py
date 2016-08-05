from enum import Enum
import datetime
import settings

class LogLevel(Enum):
	INFO = 'Info'
	WARNING = 'Warn'
	ERROR = 'Erro'

def Log(logLevel, msg):
	logString = "%s [%s]: %s " % (datetime.datetime.now().strftime("%H:%M:%S"), logLevel.value, msg)
	if settings.printLog:
		print(logString)
	if settings.logToFile:
		WriteToLog(logString)

def WriteToLog(msg):
	logFileNum = 1
	tempLogFile = settings.logFile
	while LogfileLength(tempLogFile) >= settings.maxLogSize:
		tempLogFile = settings.logFile + str(logFileNum)
		print(tempLogFile)
		logFileNum += 1

	with open(tempLogFile, 'a') as file:
		file.write(msg + '\n')

def LogfileLength(logFile):
	lines = 0
	try:
		with open(logFile, 'r') as file:
			for line in file.readlines():
				lines += 1
			return lines
	except IOError:
		return 0 # File does not exist
	except Exception as e:
		Log(LogLevel.ERROR, 'Logfile "%s" is not a file' % logFile)
