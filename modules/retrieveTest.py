from fileStorage import FileStorage
from datetime import datetime
import os
import time
import xlsxwriter

fileStorage = FileStorage()

testingFiles = '../testingFiles/'
fileNames = os.listdir(testingFiles)

workbook = xlsxwriter.Workbook('./data/retrieve.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write('A1', 'fileName')
worksheet.write('B1', 'Size')
worksheet.write('C1', 'time')
worksheet.set_column('A:C', 25)


row = 2
for file in fileNames:
	start = datetime.now()
	info = fileStorage.retrieve_from_name(file)

	diff = datetime.now() - start
	diffTime = diff.seconds+diff.microseconds/1000000
	print(diffTime)

	worksheet.write(row, 0, file)
	worksheet.write(row, 1, '')
	worksheet.write(row, 2, diffTime)
	worksheet.write(row, 3, start.strftime("%d/%m/%Y - %H:%M:%S"))
	row += 1

workbook.close()