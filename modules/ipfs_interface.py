
import ipfsapi
import urllib3
class IPFS:
	# Upload the file onto local IPFS node
	def upload(self, fileName):
		try:
			# Get the client instance of the IPFS local node
			api = ipfsapi.Client('127.0.0.1', 5001)
			# upload the file onto local node and store the hash returned
			result = api.add(fileName)
		# If the local daemon is not alive then catch the error 
		except urllib3.exceptions.NewConnectionError:
			raise Exception('Is the local IPFS Daemon running?')

		print(result)
		return result

	# Retrieve file from IPFS network through hash
	def retrieve(self, fileHash):
		try:
			# Access the entire IPFS network 
			api = ipfsapi.Client('127.0.0.1', 8080)
			# query for the file on the entire network 
			fileContents = api.cat(fileHash)
		# If the local daemon is not alive then catch the error 	
		except urllib3.exceptions.NewConnectionError:
			raise Exception('Is the local IPFS Daemon running?')
		
		return fileContents
