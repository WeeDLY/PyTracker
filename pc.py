import platform
from re import match
from netifaces import interfaces
from socket import gethostname
from uuid import getnode
import net_cap

def GetPCName():
	return gethostname()

def GetMac():
	return getnode()

def GetOS():
	os = platform.system()
	ver = platform.version()
	version = match('\S+', ver).group()

	return os + ' ' + version

def GetBit():
	return platform.architecture()[0]

def GetCPU():
	return platform.processor()

def GetPCInfo():
	pcInfo = []
	pcName = pc.GetPCName()
	OS = pc.GetOS()
	bit = pc.GetBit()
	cpu = pc.GetCPU()

	pcInfo.append(pcName)
	pcInfo.append(OS)
	pcInfo.append(bit)
	pcInfo.append(cpu)
	return pcInfo

def GetInterface():
	return GetInterfaceEnum(interfaces())

def GetInterfaceEnum(interfaces):
	interfaceEnum = []
	for interface in net_cap.interface:
		for interface_used in interfaces:
			if interface.name == interface_used:
				interfaceEnum.append(interface)
	return interfaceEnum
