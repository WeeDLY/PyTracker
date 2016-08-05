"""
Libraries needed:
  PyMySql
  psutil
  platform
  socket
  threading
  netifaces
  time

timeInterval: How often updating the uptime of the program. (Seconds)
netInterval: How often update network usage on the computer. (Seconds)
cpuInterval: How often update CPU usage on the computer. (Seconds)

useRuntime: True/False: Whether you want to store the uptime of the program.
useNetCapture: True/False: Whether you want to capture the network statistics
disallowInterface: Add interfaces you don't want to capture network statistics. i.e: interface.eth0
useCPUCapture: True/False: Whether you want to capture the CPU statistics

logToFile: True/False: Whether or not to log to a file
logFile: File the program should log Info/Warning/Errros too.
printLog: True/false: Whether the program should display log in the terminal

Database settings: Self explanatory
"""
from net_cap import interface

timeInterval = 1
netInterval = 60
cpuInterval = 60

useRuntime = True
useCPUCapture = True
useNetCapture = True
disallowInterface = []

logToFile = True
logFile = 'log_file'
printLog = True

""" Database settings """
username = ''
password = ''
server = ''
database = ''
mainTable = ''

""" Overall settings """
logRuntimeInterval = 60
maxLogSize = 500

version = '0.3'
author = 'WeeDLY'
