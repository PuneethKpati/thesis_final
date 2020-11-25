
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
		

	def openNextLog(self):
		# Read the document number for logging file
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
		worksheet.write('C1', 'pName')
		worksheet.write('D1', 'memory (Mb)')
		worksheet.write('E1', 'memusage')
		worksheet.write('F1', 'cpuTotal')
		worksheet.write('G1', 'cpuUsage')
		worksheet.set_column('A:G', 25)

		return workbook, worksheet

	# logs all the data in appropriate xlsx sheets
	def log(self, addTime):

		# log data every second for the given duration
		finish = datetime.now() + timedelta(minutes=addTime)
		while datetime.now() < finish:
			# interval timeSlot 
			endLog = datetime.now() + timedelta(hours=1)
			# If next interval is later than the finish time then end before finish
			if endLog > finish:
				endLog = finish

			# get a new workbook and start data logging from row 2
			workbook, worksheet = self.openNextLog()
			row = 2

			# for every 500ms in the next interval repeat the logging
			while(datetime.now() < endLog):
			# for each process being monitored
				for p in self.processP:
					# record current datetime
					currTime = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
					self.processP[p].cpu_percent(interval=1)
					# All our metrics are calculated here
					mem_mbs  = self.processP[p].memory_full_info().rss
					memusage = self.processP[p].memory_percent()
					cpuTotal = self.processP[p].cpu_percent(interval=1)
					cpuUsage = cpuTotal / psutil.cpu_count()
					pName = self.processP[p].name()
					# write all the current time data in the same row 
					# in their respective columns
					worksheet.write(row, 0, currTime)
					worksheet.write(row, 1, p)
					worksheet.write(row, 2, pName)
					worksheet.write(row, 3, mem_mbs)
					worksheet.write(row, 4, memusage)
					worksheet.write(row, 5, cpuTotal)
					worksheet.write(row, 6, cpuUsage)

					print('Entered data: ', pName, currTime, p, memusage, mem_mbs, cpuTotal, cpuUsage)
					row += 1

				# duration between each entry in seconds
				# time.sleep(0.5)
			# close workbook and save the file
			workbook.close()

numElem = input('Enter number of pids: ')
pids = []
for i in range(int(numElem)):
	pid = int(input('Enter Process ID (pid) : '))
	pids.append(pid)

g = DataLogger(pids)
period = input('Enter period for logging (minutes) : ')
g.log(int(period))
