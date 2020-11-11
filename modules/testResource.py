from resource_manager import ResourceManager
import time 

r = ResourceManager(10, 10, 'A')

time.sleep(8)
r.addNewFile('haha')