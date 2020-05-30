# File for Marwa
# 18/11/2019
import time
import json, codecs
time_start = time.clock()
import os, cs

# First we make sure the external twitter scraping tool is available
# After the first run you can comment this part
print("Installing twint...")
command="pip install twint"
os.system(command)





users=[]  #here is where all usernames should be stored e.g. ['username1', 'username2']
folder=''  #Write here the name of the folder where to store them

full_profile=False # Some times there are hidden tweets, if you observe that you cant get all of them, 
				   # change this to True
k=0
for f in users:
	#Checks if we hae downloaded it already
	k=k+1
	print('Username '+str(k)+' of '+str(len(users)))
	if not os.path.exists(folder+"\\"+f+".csv"):
		if full_profile:
			command="twint -u "+f+" -o "+folder+"\\"+f+".csv --csv --profile-full --hide-output"
		else:
			command="twint -u "+f+" -o "+folder+"\\"+f+".csv --csv --hide-output"
		os.system(command)
		print('Username '+f+' downloaded')
	else:
		print('Username '+f+' already in memory')


time_elapsed = (time.clock() - time_start)
print("Total time elapsed ",time_elapsed/3600," hours")