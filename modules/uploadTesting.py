from fileStorage import FileStorage
from datetime import datetime
import os
import time
import xlsxwriter

fileStorage = FileStorage()
testingFiles = '../testingFiles/'
fileNames = os.listdir(testingFiles)

workbook = xlsxwriter.Workbook('./data/upload.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write('A1', 'fileName')
worksheet.write('B1', 'Size')
worksheet.write('C1', 'time')
worksheet.set_column('A:C', 25)

row = 2
for file in fileNames:
	filePath = testingFiles+file

	start = datetime.now()
	info = fileStorage.upload(filePath)

	diff = datetime.now() - start
	diffTime = diff.seconds+diff.microseconds/1000000
	print(diffTime)

	worksheet.write(row, 0, file)
	worksheet.write(row, 1, info['Size'])
	worksheet.write(row, 2, diffTime)

	row += 1

workbook.close()