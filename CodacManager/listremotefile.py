
#!/usr/bin/env python 

import pysftp

srv = pysftp.Connection(host="10.136.64.112", username="codac-dev",password="core09")
# Get the directory and file listing
data = srv.listdir()
# Closes the connection
srv.close()
# Prints out the directories and files, line by line
for i in data:
	print i
