import os 

sizes = ['100K', '500K', '1M', '5M', '10M']

for size in sizes:
	for count in range(30):
		os.system(f'truncate -s {size} {size}_{count}.txt')