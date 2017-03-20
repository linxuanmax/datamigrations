import os 
dir_name = os.path.dirname(__file__)
print dir_name 
if dir_name != '':
	os.chdir(dir_name)
print dir_name
