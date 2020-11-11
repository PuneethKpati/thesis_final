from fileStorage import FileStorage

fileStorage = FileStorage()
while True:
	print('\n')
	fileName = input("Uploading File's Name: ")
# try:
	info = fileStorage.upload(fileName)
# except:
	print('Not a Valid File!')
