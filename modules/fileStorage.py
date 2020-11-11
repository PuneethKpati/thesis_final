
from ipfs_interface import IPFS
from ipfs_contract_interface import Contract

class FileStorage:

	def __init__(self):
		# storing the names of files stored
		self.files = []
		# storing the instances of IPFS and contract objects
		# to access the tools through custom interfaces
		self.ipfs = IPFS()
		self.ipfsContract = Contract()

	# upload the file 
	def upload(self, fileName):
		print('Uploading File On IPFS Network')
		# Upload profile onto Ipfs
		fileInfo = self.ipfs.upload(fileName)

		print('Uploading File Hash To IPFS contract ...')
		# upload the ipfs hash onto ethereum smart contract
		self.ipfsContract.addFile(fileInfo['Name'], fileInfo['Hash'])
		# add to the list of files from current node
		self.files.append(fileName)

		return fileInfo

	# Retrieving file from the FileName
	def retrieve_from_name(self, fileName):
		print('Retrieving Hash From IPFS contract ...')
		# If we don't have the hash for the file then retrieve from IPFS
		fileHash = self.ipfsContract.retrieveHash(fileName)

		print('Retrieving File From IPFS Network Through Hash ...')
		# retrieve file content through class's internal function
		fileContents = self.retrieve_from_hash(fileHash)
		print(fileContents)
		return fileContents

	# Retrieving file from the file hash 
	def retrieve_from_hash(self, fileHash):
		return self.ipfs.retrieve(fileHash)

