import db, settings

def CreateDatabase():
	return 'CREATE database %s' % settings.database

def CreateMainTable():
	return """
		CREATE TABLE %s(
			ID TINYINT AUTO_INCREMENT NOT NULL PRIMARY KEY,
			PCName VARCHAR(32),
			TableNet VARCHAR (32),
			TableCPU VARCHAR (32),
			Mac BIGINT,
			OS VARCHAR(64),
			PCBit VARCHAR(8),
			Runtime TIME,
			CPU VARCHAR(64)
			)""" % (settings.mainTable)

def CreateTableNet(pcName):
	return """
		CREATE TABLE """ + pcName + """(
		startTime TIME,
		stopTime TIME,
		startDate DATE,
		stopDate DATE,
		interface VARCHAR(16),
		bytes_sent BIGINT,
		bytes_recv BIGINT,
		packets_sent MEDIUMINT,
		packets_recv MEDIUMINT,
		errin SMALLINT,
		errout SMALLINT,
		dropin SMALLINT,
		dropout SMALLINT
		) """

def CreateTableCPU(pcName):
	return """
		CREATE TABLE """ + pcName + """(
		date DATE,
		time TIME,
		total BIGINT,
		available BIGINT,
		used BIGINT,
		percent FLOAT
		)
	"""

def InsertMainTable(currentPC):
	query = """ INSERT INTO %s(PCName, TableNet, TableCPU, Mac, OS, PCBit, Runtime, CPU)
				VALUES("%s", "%s", "%s", %d, "%s", "%s", "%s", "%s") """
	return query % (settings.mainTable, currentPC.PCName, currentPC.TableNet, currentPC.TableCPU, currentPC.Mac, currentPC.OS, currentPC.PCBit, '0:0:0', currentPC.CPU)

def InsertNetTable(currentPC, startSession, captureSession):
	query = """ INSERT INTO %s(startTime, stopTime, startDate, stopDate, interface, bytes_sent, bytes_recv, packets_sent, packets_recv, errin, errout, dropin, dropout)
				VALUES (%s, %s, %s, %s, "%s", %d, %d, %d, %d, %d, %d, %d, %d) """
	return query % (currentPC.TableNet, str(startSession.startTime), str(captureSession.startTime), str(startSession.startDate), str(captureSession.startDate), startSession.interface.value, captureSession.bytes_sent, captureSession.bytes_recv, captureSession.packets_sent, captureSession.packets_recv, captureSession.errin, captureSession.errout, captureSession.dropin, captureSession.dropout)

def InsertCPUTable(currentPC, CPUSession):
	query = """ INSERT INTO %s(date, time, total, available, used, percent)
				VALUES ('%s', '%s', %d, %d, %d, %f)"""
	return query % (currentPC.TableCPU, str(CPUSession.date), str(CPUSession.time), CPUSession.total, CPUSession.available, CPUSession.used, CPUSession.percent)

def GetMainTable():
	return 'SELECT * FROM %s' % (settings.mainTable)

def GetPCName():
	return 'SELECT PCName from %s' % (settings.mainTable)

def TableExists(table):
	#return 'SELECT * FROM information_schema.tables WHERE table_name = "%s"' % (table)
	return 'SHOW TABLES LIKE "%s"' % (table)

def GetID(currentPC):
	query = """ SELECT ID FROM %s
	WHERE PCName LIKE '%s'
	AND TableNet LIKE '%s'
	AND Mac LIKE %d
	AND OS LIKE '%s'
	AND PCBit LIKE '%s'
	AND CPU LIKE '%s' """
	return query % (settings.mainTable, currentPC.PCName, currentPC.TableNet, currentPC.Mac, currentPC.OS, currentPC.PCBit, currentPC.CPU)

def GetRuntime(pcID):
	query = """ SELECT Runtime FROM %s
	where ID like %d """
	return query % (settings.mainTable, pcID)

def UpdateRuntime(currentPC, runtime):
	query = """ UPDATE %s
			SET Runtime='%s'
			WHERE ID like %d """
	return query % (settings.mainTable, runtime, currentPC.ID)

def PCAlreadyExists(currentPC):
	query = """ SELECT * FROM %s
	WHERE PCName LIKE '%s'
	AND Mac LIKE %d
	AND OS LIKE '%s'
	AND PCBit LIKE '%s'
	AND CPU LIKE '%s' """
	return query % (settings.mainTable, currentPC.PCName, currentPC.Mac, currentPC.OS, currentPC.PCBit, currentPC.CPU)
