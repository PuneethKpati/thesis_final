import psutil
import json
import threading
import time
from web3.geth import shh
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware

from fileStorage import FileStorage

class ResourceManager:

	def __init__(self, cpu, mem):
		self.cpu_roof = cpu
		self.mem_roof = mem
		self.newFileHash = ''
		self.helpAsked = False
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

    # Broadcasts a message to network for hhelp 
	def askHelp(self):
		self.web3.geth.shh.post({'payload': self.web3.toHex(text="HELP\r\n"+ self.newFileHash), 'symKeyID': self.sym_key_id, 'topic': '0x12340000', 'powTarget': 0, 'powTime': 2})
		self.helpAsked = True

	# If a profile has been processed, broadcasts the message a FIN signal
	def sendHelp(self, fileHash):
		self.web3.geth.shh.post({'payload': self.web3.toHex(text="FIN\r\n"+ fileHash), 'symKeyID': self.sym_key_id, 'topic': '0x12340000', 'powTarget': 0, 'powTime': 2})
		

	# watches the network for broadcast messages on the topic filter
	def monitorFilter(self):
		while True:
			# get current messages
			messages = self.web3.geth.shh.get_filter_messages(self.filter_id)
			print('polling...')

			# go through all messages active right now
			for message in messages:
				content = message['payload']
				contentS = bytes.fromhex(content.hex()[2:]).decode('utf-8')
				Header, fileHash = contentS.split('\r\n')
				print(Header, fileHash, '\n\n\n\n\n')
				# If help is needed and device has enough resources - sendHelp
				if Header == 'HELP':
					if not self.busy():
						self.sendHelp(fileHash)

					fs = FileStorage()
					# fs.retrieve_from_hash(fileHash)

				# If our help request has been pushed by someone then release job
				elif Header == 'FIN':
					if self.newFileHash == fileHash:
						self.newFileHash = ''
						self.helpAsked = False

			time.sleep(1)

			

	# monitor the performance for each call
	def monitorPerformance(self):
		while True:
			if self.newFileHash and not self.helpAsked:
				if self.busy():
					self.askHelp()

			time.sleep(1)

	# determines whether a given node is busy or not
	def busy(self):
		cpuUsage = psutil.cpu_percent(interval=1)
		memUsage = psutil.virtual_memory().percent
		if cpuUsage > self.cpu_roof or memUsage > self.mem_roof:
			return True
		return False

	def addNewFile(self, newFile):
		self.newFileHash = newFile



