import json
from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware

class Contract:
	def __init__(self):

		# for now lets use the development server on ganache
		web = 'http://127.0.0.1:8545'
		# Get the client instance to interact with our ethereum network
		self.web3 = Web3(HTTPProvider(web))

		# inject the poa compatibility middleware to the innermost layer
		self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)

		# set the default account for prototype
		self.web3.eth.defaultAccount = self.web3.eth.accounts[0]
		# IF the contract file exists, retrieve smart contract details

		try:
			file = open('./../truffle/build/contracts/Ipfs.json', 'r')
			contract_json = json.load(file)
			# Retrive the abi for the contract contents
			self.contract_abi = contract_json['abi'] 
			# Retrieve the address of the deployed contract on the network
			self.contract_address = contract_json['networks']['1']['address']

		# If the file doesn't exist then stop the process
		except IOError:
			raise Exception('File does not exist, has the contract been loaded?')

		# Else get an instance of the contract to begin storing and retrieving hashes
		else:
			self.ipfsHashes = self.web3.eth.contract(address=self.contract_address, abi=self.contract_abi)
			print(self.ipfsHashes)

	# Adds the ipfs hash of a given file into the smart contract mapping
	def addFile(self, fileId, ipfsHash):
		# create a new transaction to store the data on the smart contract
		# store the return value (transaction hash) for retrieving the receipt
		tx_hash = self.ipfsHashes.functions.addHash(fileId, ipfsHash).transact()
		receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)

		return receipt

	# Retrieves the hash of a given file added to the smart contract
	def retrieveHash(self, fileId): 
		# IF file id is not a valid string
		if not isinstance(fileId, str):
			return None

		# return the hash value from the smart contract storage 
		return self.ipfsHashes.functions.getHash(fileId).call()


