import psutil
import json
import thread
from web3.geth import shh
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware

class ResourceManager:

	def __init__(self, cpu, mem):
		self.cpu_roof = cpu
		self.mem_roof = mem

		try:
		   thread.start_new_thread( self.monitorPerformance)
		   thread.start_new_thread( self.monitorFilter )
		except:
		   print "Error: unable to start thread"

	def askHelp(self):
		pass

	def sendHelp(self, sender):
		pass

	def monitorFilter(self):
		pass

	def monitorPerformance(self):
		pass