
import xlsxwriter
import datetime
import time
from datetime import datetime, timedelta
import psutil 
import sys

class DataLogger:
	def __init__(self, pids):
		self.pid = pids
		self.processP = {}
		for pid in pids:
			self.processP[pid] = psutil.Process(pid)
		
	# logs all the data in appropriate xlsx sheets
	def log(self, addTime):
		with open("data/num", "r+") as f:
		    data = f.read()
		    docNum = int(data)
		    f.seek(0)
		    f.write(str(docNum+1))
		    f.truncate()

		# setup the excel workbook and worksheet
		workbook = xlsxwriter.Workbook('data/data' + str(docNum) + '.xlsx')
		worksheet = workbook.add_worksheet()
		worksheet.write('A1', 'Time')
		worksheet.write('B1', 'pid')
		worksheet.write('C1', 'memory (Mb)')
		worksheet.write('D1', 'memusage')
		worksheet.write('E1', 'cpuTotal')
		worksheet.write('F1', 'cpuUsage')
		worksheet.set_column('A:F', 25)

		# enter data from row2
		row = 2
		# log data every second for the given duration
		finish = datetime.now() + timedelta(hours=addTime)
		while datetime.now() < finish:
			# for each process being monitored
			for p in self.processP:
				# record current datetime
				currTime = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")

				# All our metrics are calculated here
				mem_mbs  = self.processP[p].memory_full_info().rss
				memusage = self.processP[p].memory_percent()
				cpuTotal = self.processP[p].cpu_percent()
				cpuUsage = cpuTotal / psutil.cpu_count()

				# write all the current time data in the same row 
				# in their respective columns
				worksheet.write(row, 0, currTime)
				worksheet.write(row, 1, p)
				worksheet.write(row, 2, mem_mbs)
				worksheet.write(row, 3, memusage)
				worksheet.write(row, 4, cpuTotal)
				worksheet.write(row, 5, cpuUsage)

				print('Entered data: ', currTime, p, memusage, mem_mbs, cpuTotal, cpuUsage)
				row += 1

			# duration between each entry in seconds
			time.sleep(0.5)
		# close workbook and save the file
		workbook.close()

numElem = input('Enter number of pids: ')
pids = []
for i in range(int(numElem)):
	pid = int(input('Enter Process ID (pid) : '))
	pids.append(pid)

g = DataLogger(pids)
period = input('Enter period for logging (hours) : ')
g.log(int(period))
