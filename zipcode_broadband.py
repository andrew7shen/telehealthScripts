#Andrew Shen, 12/13/21
#Script to perform zipcode and broadband analysis for telehealth project, exploring other variables
#To run: python zipcode_broadband.py
#Ex: python3 zipcode_broadband.py

import sys
import re
from haversine import haversine, Unit

#Read in masterTable files
with open("/Users/andrewshen/Desktop/masterTables/masterTable2019.txt", 'r') as file:
	masterTable2019_contents = file.readlines() #format: each item is a different line
for i in range(len(masterTable2019_contents)):
	curr = masterTable2019_contents[i]
	split_line = curr.strip() #get rid of \n
	split_line = split_line.split("\t")
	masterTable2019_contents[i] = split_line #format: each item composed of values separated by tabs


with open("/Users/andrewshen/Desktop/masterTables/masterTable2020.txt", 'r') as file:
	masterTable2020_contents = file.readlines() #format: each item is a different line
for i in range(len(masterTable2020_contents)):
	curr = masterTable2020_contents[i]
	split_line = curr.strip() #get rid of \n
	split_line = split_line.split("\t")
	masterTable2020_contents[i] = split_line #format: each item composed of values separated by tabs


with open("/Users/andrewshen/Desktop/masterTables/masterTable2021.txt", 'r') as file:
	masterTable2021_contents = file.readlines() #format: each item is a different line
for i in range(len(masterTable2021_contents)):
	curr = masterTable2021_contents[i]
	split_line = curr.strip() #get rid of \n
	split_line = split_line.split("\t")
	masterTable2021_contents[i] = split_line #format: each item composed of values separated by tabs


with open("/Users/andrewshen/Desktop/coord_distances.csv", 'r') as file:
	coord_distances = file.readlines()
for i in range(len(coord_distances)):
	curr = coord_distances[i]
	split_line = curr.strip() #get rid of \n
	split_line = split_line.split(",")
	coord_distances[i] = split_line

with open("/Users/andrewshen/Desktop/broadband_usage.csv", 'r') as file:
	broadband_usage = file.readlines()
for i in range(len(broadband_usage)):
	curr = broadband_usage[i]
	split_line = curr.strip() #get rid of \n
	split_line = split_line.split(",")
	broadband_usage[i] = split_line





# with open("/Users/andrewshen/Desktop/tele2019/demographics2019_3.15-3.20.csv", 'r') as file:
# 	info_contents = file.readlines() #format: each item is a different line
# for i in range(len(info_contents)):
# 	curr = info_contents[i]
# 	split_line = curr.strip() #get rid of \n
# 	result = re.split(r'(?<![A-Z]),', split_line, flags=re.I)
# 	info_contents[i] = result
# dtest = open("/Users/andrewshen/Desktop/demTest.txt", "w")
# dtestStr = ""
# final_dTot = ""
# for i in range(len(info_contents)):
# 	curr = info_contents[i]
# 	for j in range(len(curr)):
# 		final_dTot += curr[j]
# 		if(j!=len(curr)): final_dTot += "\t"
# 	if(i!=len(info_contents)): final_dTot += "\n"
# dtest.writelines(final_dTot)
# dtest.close()





#Frequency analysis for zipcodes, index 56 in masterTables
zip_original = "Zipcode\tFreq\tYear\n"
zip_onlyFive = "Zipcode\tFreq\tYear\tDistance\tBroadband\n"


#For original zipcodes and zipcodes of length five
stats2019_dict = {} #dictionary with zipcodes as the keys
stats2019_dict5 = {}
for i in range(1,len(masterTable2019_contents)):
	currZip = masterTable2019_contents[i][56]
	#print currZip
	if(currZip not in stats2019_dict): stats2019_dict[currZip] = 1
	else: stats2019_dict[currZip] = stats2019_dict[currZip] + 1
	editedZip = ""
	if(len(currZip)==5): editedZip = currZip
	elif(len(currZip)>5): editedZip = currZip[0:5]
	else: editedZip = "ERROR"
	if(editedZip not in stats2019_dict5): stats2019_dict5[editedZip] = 1
	else: stats2019_dict5[editedZip] = stats2019_dict5[editedZip] + 1

stats2020_dict = {}
stats2020_dict5 = {}
for i in range(1,len(masterTable2020_contents)):
	currZip = masterTable2020_contents[i][56]
	#print currZip
	if(currZip not in stats2020_dict): stats2020_dict[currZip] = 1
	else: stats2020_dict[currZip] = stats2020_dict[currZip] + 1
	editedZip = ""
	if(len(currZip)==5): editedZip = currZip
	elif(len(currZip)>5): editedZip = currZip[0:5]
	else: editedZip = "ERROR"
	if(editedZip not in stats2020_dict5): stats2020_dict5[editedZip] = 1
	else: stats2020_dict5[editedZip] = stats2020_dict5[editedZip] + 1

stats2021_dict = {}
stats2021_dict5 = {}
for i in range(1,len(masterTable2021_contents)):
	currZip = masterTable2021_contents[i][56]
	#print currZip
	if(currZip not in stats2021_dict): stats2021_dict[currZip] = 1
	else: stats2021_dict[currZip] = stats2021_dict[currZip] + 1
	editedZip = ""
	if(len(currZip)==5): editedZip = currZip
	elif(len(currZip)>5): editedZip = currZip[0:5]
	else: editedZip = "ERROR"
	if(editedZip not in stats2021_dict5): stats2021_dict5[editedZip] = 1
	else: stats2021_dict5[editedZip] = stats2021_dict5[editedZip] + 1

#for k,v in stats2019_dict.iteritems():
#	print "k: %s, v: %d" % (k,v)

#Run haversine
clinic = (37.44870,-122.12054) #Zipcode 94303
home = (37.18614197, -121.8435516) #Zipcode 95120
haversine2019_dict = {}
haversine2020_dict = {}
haversine2021_dict = {}
# #print(haversine(clinic, home,unit=Unit.MILES))
# for key in stats2019_dict5:
# 	latitude = 0.0
# 	longitude = 0.0
# 	#found = False
# 	for i in range(1,len(coord_distances)):
# 		curr = coord_distances[i]
# 		if(str(curr[2])==key):
# 			latitude = float(curr[0])
# 			longitude = float(curr[1])
# 			#found = True
# 	currLocation = (latitude, longitude)
# 	# if(found == True): haversine_dict[key] = haversine(clinic, currLocation, unit=Unit.MILES)
# 	# else: haversine_dict[key] = "NOTFOUND"
# 	haversine2019_dict[key] = haversine(clinic, currLocation, unit=Unit.MILES)

for key in stats2019_dict5:
	latitude = 0.0
	longitude = 0.0
	found = False
	for i in range(1,len(coord_distances)):
		curr = coord_distances[i]
		if(str(curr[2])==key):
			latitude = float(curr[0])
			longitude = float(curr[1])
			found = True
	currLocation = (latitude, longitude)
	if(found == True): haversine2019_dict[key] = haversine(clinic, currLocation, unit=Unit.MILES)
	else: haversine2019_dict[key] = ""

for key in stats2020_dict5:
	latitude = 0.0
	longitude = 0.0
	found = False
	for i in range(1,len(coord_distances)):
		curr = coord_distances[i]
		if(str(curr[2])==key):
			latitude = float(curr[0])
			longitude = float(curr[1])
			found = True
	currLocation = (latitude, longitude)
	if(found == True): haversine2020_dict[key] = haversine(clinic, currLocation, unit=Unit.MILES)
	else: haversine2020_dict[key] = ""

for key in stats2021_dict5:
	latitude = 0.0
	longitude = 0.0
	found = False
	for i in range(1,len(coord_distances)):
		curr = coord_distances[i]
		if(str(curr[2])==key):
			latitude = float(curr[0])
			longitude = float(curr[1])
			found = True
	currLocation = (latitude, longitude)
	if(found == True): haversine2021_dict[key] = haversine(clinic, currLocation, unit=Unit.MILES)
	else: haversine2021_dict[key] = ""


#Match up zipcodes to broadband usage
broadband2019_dict = {}
broadband2020_dict = {}
broadband2021_dict = {}
for key in stats2019_dict5:
	found = False
	for i in range(1,len(broadband_usage)):
		curr = broadband_usage[i]
		if(curr[3] == key): 
			broadband2019_dict[key] = curr[4]
			found = True
	if(found == False): broadband2019_dict[key] = ""

for key in stats2020_dict5:
	found = False
	for i in range(1,len(broadband_usage)):
		curr = broadband_usage[i]
		if(curr[3] == key):
			broadband2020_dict[key] = curr[4]
			found = True
	if(found == False): broadband2020_dict[key] = ""

for key in stats2021_dict5:
	found = False
	for i in range(1,len(broadband_usage)):
		curr = broadband_usage[i]
		if(curr[3] == key):
			broadband2021_dict[key] = curr[4]
			found = True
	if(found == False): broadband2021_dict[key] = ""

#Creating output file content
for k,v in stats2019_dict.items():
	toAdd = k + "\t" + str(v) + "\t2019\n"
	zip_original += toAdd
for k,v in stats2020_dict.items():
	toAdd = k + "\t" + str(v) + "\t2020\n"
	zip_original += toAdd
for k,v in stats2021_dict.items():
	toAdd = k + "\t" + str(v) + "\t2021\n"
	zip_original += toAdd

for k,v in stats2019_dict5.items():
	toAdd = k + "\t" + str(v) + "\t2019\t" + str(haversine2019_dict[k]) + "\t" + str(broadband2019_dict[k]) + "\n"
	zip_onlyFive += toAdd
for k,v in stats2020_dict5.items():
	toAdd = k + "\t" + str(v) + "\t2020\t" + str(haversine2020_dict[k]) + "\t" + str(broadband2020_dict[k]) + "\n"
	zip_onlyFive += toAdd
for k,v in stats2021_dict5.items():
	toAdd = k + "\t" + str(v) + "\t2021\t" + str(haversine2021_dict[k]) + "\t" + str(broadband2021_dict[k]) + "\n"
	zip_onlyFive += toAdd



#Write zipcode information to output file
zip_out = open("/Users/andrewshen/Desktop/zipFreqsOrig.txt", "w")
zip_outStr = ""
zip_outStr = zip_original
zip_out.writelines(zip_outStr)
zip_out.close()
print ("File zipFreqsOrig.txt was created.")

zip_out = open("/Users/andrewshen/Desktop/zipFreqsFive.txt", "w")
zip_outStr = ""
zip_outStr = zip_onlyFive
zip_out.writelines(zip_outStr)
zip_out.close()
print ("File zipFreqsFive.txt was created.")


#Add info to masterTables
for i in range(1,len(masterTable2019_contents)):
	curr = masterTable2019_contents[i]
	zipcode = ""
	if(len(curr[56])>4):
		zipcode = curr[56][:5]
		masterTable2019_contents[i].append(str(haversine2019_dict[zipcode]))
		masterTable2019_contents[i].append(str(broadband2019_dict[zipcode]))
	else:
		masterTable2019_contents[i].append("blank")
		masterTable2019_contents[i].append("blank")
for i in range(1,len(masterTable2020_contents)):
	curr = masterTable2020_contents[i]
	zipcode = ""
	if(len(curr[56])>4):
		zipcode = curr[56][:5]
		masterTable2020_contents[i].append(str(haversine2020_dict[zipcode]))
		masterTable2020_contents[i].append(str(broadband2020_dict[zipcode]))
	else:
		masterTable2020_contents[i].append("blank")
		masterTable2020_contents[i].append("blank")
for i in range(1,len(masterTable2021_contents)):
	curr = masterTable2021_contents[i]
	zipcode = ""
	if(len(curr[56])>4):
		zipcode = curr[56][:5]
		masterTable2021_contents[i].append(str(haversine2021_dict[zipcode]))
		masterTable2021_contents[i].append(str(broadband2021_dict[zipcode]))
	else:
		masterTable2021_contents[i].append("blank")
		masterTable2021_contents[i].append("blank")

#Write to masterTables
new2019 = open("/Users/andrewshen/Desktop/newMasterTable2019.txt", "w")
new2019Str = ""
masterTable2019_contents[0].append("Distance")
masterTable2019_contents[0].append("Broadband")
new2019Str = masterTable2019_contents
out2019 = ""
for i in range(len(new2019Str)):
	curr = new2019Str[i]
	for j in range(len(curr)):
		out2019 += curr[j]
		if(j!=len(curr)): out2019 += "\t"
	if(i!=len(new2019Str)): out2019 += "\n"
new2019.writelines(out2019)
new2019.close()
print ("File newMasterTable2019.txt was created.")

new2020 = open("/Users/andrewshen/Desktop/newMasterTable2020.txt", "w")
new2020Str = ""
masterTable2020_contents[0].append("Distance")
masterTable2020_contents[0].append("Broadband")
new2020Str = masterTable2020_contents
out2020 = ""
for i in range(len(new2020Str)):
	curr = new2020Str[i]
	for j in range(len(curr)):
		out2020 += curr[j]
		if(j!=len(curr)): out2020 += "\t"
	if(i!=len(new2020Str)): out2020 += "\n"
new2020.writelines(out2020)
new2020.close()
print ("File newMasterTable2020.txt was created.")

new2021 = open("/Users/andrewshen/Desktop/newMasterTable2021.txt", "w")
new2021Str = ""
masterTable2021_contents[0].append("Distance")
masterTable2021_contents[0].append("Broadband")
new2021Str = masterTable2021_contents
out2021 = ""
for i in range(len(new2021Str)):
	curr = new2021Str[i]
	for j in range(len(curr)):
		out2021 += curr[j]
		if(j!=len(curr)): out2021 += "\t"
	if(i!=len(new2021Str)): out2021 += "\n"
new2021.writelines(out2021)
new2021.close()
print ("File newMasterTable2021.txt was created.")

















