import os 

sizes = ['100K', '500K', '1M', '5M', '10M']

XPS = open('XPSFiles', 'w')
R1 = open('R1Files', 'w')
R2 = open('R2Files', 'w')
for size in sizes:
	for count in range(30):
		os.system(f'truncate -s {size} {size}B_{count}.txt')
		print(f'{size}B_{count}.txt')
		XPS.write(f'{size}B_{count}.txt')
		R1.write(f'{size}B_{count}_R.txt')
		R2.write(f'{size}B_{count}_R2.txt')

XPS.close()
R1.close()
R2.close()