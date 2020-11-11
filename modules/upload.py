from fileStorage import FileStorage

fileStorage = FileStorage()
while True:
	print('\n')
	fileName = input("Uploading File's Name: ")

	info = fileStorage.upload(fileName)
	print(info)
