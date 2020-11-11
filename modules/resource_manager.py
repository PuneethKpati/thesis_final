import psutil
import json
import threading
import time
from web3.geth import shh
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware

class ResourceManager:

	def __init__(self, cpu, mem):
		self.cpu_roof = cpu
		self.mem_roof = mem

		# for now lets use the development server on ganache
		web = 'http://127.0.0.1:8545'
		# Get the client instance to interact with our ethereum network
		self.web3 = Web3(HTTPProvider(web))

		# inject the poa compatibility middleware to the innermost layer
		self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)

		# since we aren't using PoW
		self.web3.geth.shh.set_min_pow(0)

		# generate a symmetric Key with shared password
		gen = self.web3.geth.shh.generate_sym_key_from_password('thesis')
		self.sym_key = self.web3.geth.shh.get_sym_key(gen)
		self.sym_key_id = self.web3.geth.shh.add_sym_key(self.sym_key)

		self.filter_id = self.web3.geth.shh.new_message_filter({'topic': '0x12340000', 'symKeyID': self.sym_key_id, 'allowP2P': True})


		try:
		   monitorPerformance = threading.Thread(target=self.monitorPerformance)
		   monitorPerformance.start()

		   monitorFilter = threading.Thread(target=self.monitorFilter)
		   monitorFilter.start()
		except:
		   print("Error: unable to start thread")

	def askHelp(self):
		self.web3.geth.shh.post({'payload': self.web3.toHex(text="HELP!"), 'symKeyID': self.sym_key_id, 'topic': '0x12340000', 'powTarget': 0, 'powTime': 2})

	def sendHelp(self, sender):
		pass

	def sendFile(self, fileName):
		self.web3.geth.shh.post({'payload': self.web3.toHex(text=fileName), 'symKeyID': self.sym_key_id, 'topic': '0x12340000', 'powTarget': 0, 'powTime': 2}) 

	def monitorFilter(self):
		while True:
			time.sleep(1)
			messages = self.web3.geth.shh.get_filter_messages(self.filter_id)

			if len(messages) > 0:
				print(messages)

	def monitorPerformance(self):
		while True:
			cpuUsage = psutil.cpu_percent(interval=1)
			memUsage = psutil.virtual_memory().percent

			if cpuUsage > self.cpu_roof or memUsage > self.mem_roof:
				print(cpu)
				print('Need Help!')
				self.askHelp()

			time.sleep(1)


r = ResourceManager(90, 90)
time.sleep(8)
r.askHelp()
