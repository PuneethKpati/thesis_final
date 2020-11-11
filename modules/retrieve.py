from fileStorage import FileStorage

fileStorage = FileStorage()
while True:
	print('')
	fileName = input("Retrieving File's Name: ")
	
	info = fileStorage.retrieve_from_name(fileName)
	print(str(info, 'utf-8'))
	
	print('\nNot a Valid File!')
	