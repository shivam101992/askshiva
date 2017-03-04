import subprocess
#subprocess.call(" python script2.py 1", shell=True
for folder in range(0, 75, 75):
	command = "python bulkIndexer.py " + str(folder) + " " + str(folder + 74)
	print command
	subprocess.call(command, shell = True)