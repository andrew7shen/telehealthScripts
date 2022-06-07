#Andrew Shen, 08/23/21
#Script to assemble the master merged table with encounter, diagnosis, and master patient info
#To run: python create_masterTable.py <path to encounter out file> <path to diagnosis out file> <path to master patient info file> <name of output file>
#Ex: python create_masterTable.py /Users/andrewshen/Desktop/encounters_mediumMRNs.csv /Users/andrewshen/Desktop/out_1_3_2.txt /Users/andrewshen/Desktop/master_info_mediumMRNs.csv masterTable_medium.txt



import sys
import re

encounters_in = sys.argv[1]
diagnosis_in = sys.argv[2]
info_in = sys.argv[3]
output_name = sys.argv[4]


#Read in input files
with open(encounters_in, 'r') as file:
	encounters_contents = file.readlines() #format: each item is a different line
for i in range(len(encounters_contents)):
	curr = encounters_contents[i]
	split_line = curr.strip() #get rid of \n
	#result = re.split(r"\",|,\"|,,", split_line)
	#KEEP FOR FUTURE result = re.split(r'(?<![A-Z]),', split_line, flags=re.I) #splits by comma, unless preceded by a letter (GOOD)
	split_line = split_line.split("\t")
	encounters_contents[i] = split_line
	#if(len(split_line) != 26): print split_line

for i in range(len(encounters_contents)):
	curr = encounters_contents[i]
	for j in range(len(curr)):
		if(curr[j]=='""' or curr[j]==''): encounters_contents[i][j] = "blank"
		else: encounters_contents[i][j] = curr[j].replace('"', '')

#for line in encounters_contents:
	#if len(line)!=24:
#		print line
#		print len(line)
	#print len(line)

with open(diagnosis_in, 'r') as file:
	diagnosis_contents = file.readlines() #format: each item is a different line
for i in range(len(diagnosis_contents)):
	curr = diagnosis_contents[i]
	split_line = curr.strip() #get rid of \n
	split_line = split_line.split("\t")
	diagnosis_contents[i] = split_line #format: each item composed of values separated by tabs





#Original
# with open(info_in, 'r') as file:
# 	info_contents = file.readlines() #format: each item is a different line
# for i in range(len(info_contents)):
# 	curr = info_contents[i]
# 	split_line = curr.strip() #get rid of \n
# 	result = re.split(r'(?<![A-Z]),', split_line, flags=re.I)
# 	info_contents[i] = result


#Experiment
with open(info_in, 'r') as file:
	info_contents = file.readlines() #format: each item is a different line
for i in range(len(info_contents)):
	curr = info_contents[i]
	split_line = curr.strip() #get rid of \n
	result = split_line.split('","')
	info_contents[i] = result

#
# for i in range(len(info_contents)):
# 	#info_contents[i][19] = info_contents[i][19].replace("\t", '')
# 	if(len(info_contents[i])==26): 
# 		print info_contents[i][19] + " ||| " + info_contents[i][20]
# 	#print len(info_contents[i])
# #






for i in range(len(info_contents)):
	curr = info_contents[i]
	for j in range(len(curr)):
		if(curr[j]=='""' or curr[j]==''): info_contents[i][j] = "blank"
		else: info_contents[i][j] = curr[j].replace('"', '')


#Start assembling master merged table
final_contents = encounters_contents
final_contents[0].insert(21, "Provider")
for i in range(len(final_contents)):
	curr = final_contents[i]
	if(len(curr) != 26): final_contents[i].insert(21, "blank")
for i in range(len(final_contents)):
	del(final_contents[i][21])

# for line in final_contents:
# 	if(len(line) != 26): print line


allCodes = []
#Match diagnoses to encounters
for i in range(len(encounters_contents)):
	currEncounter = encounters_contents[i]
	#print len(currEncounter)
	#print currEncounter
	encounterCode = currEncounter[23]
	diagnosisMatch = False
	for j in range(len(diagnosis_contents)):
		currDiagnosis = diagnosis_contents[j]
		diagnosisCode = currDiagnosis[10]
		#print diagnosisCode #some are PatEnsEncCoded???
		if(encounterCode == diagnosisCode and encounterCode not in allCodes): #add diagnosis if PatEnsEncCoded match
			#final_contents[i] += currDiagnosis
			#for k in range(len(diagnosis_contents)):
			#	final_contents += diagnosis_contents[k]
			#	if(k!=len(currDiagnosis)): final_contents += "\t"
			#if(i!=len(encounters_contents)): final_contents[i] += "\n"
			for k in range(3,10):
				#print currDiagnosis[k]
				final_contents[i].append(currDiagnosis[k])
			diagnosisMatch = True
			allCodes.append(encounterCode)
			#final_contents[i]
	if(diagnosisMatch == False): #add x number of empty values if PatEnsEncCoded don't match
		numberOfDiagnosesValues = 7
		for k in range(numberOfDiagnosesValues):
			final_contents[i].append("blank")

#Match master patient info
for i in range(len(encounters_contents)):
	currEncounter = encounters_contents[i]
	encounterID = currEncounter[0]
	#print currEncounter
	#print len(currEncounter)
	found = False
	for j in range(len(info_contents)):
		currInfo = info_contents[j]
		infoID = currInfo[0]
		if(encounterID == infoID):
			for k in range(1,25):
				final_contents[i].append(currInfo[k])
			found = True
	if(found == False):
		for k in range(1,25):
			final_contents[i].append("blank")

final_contents[0].append("Period")
for i in range(len(encounters_contents)):
	if(i != 0):
		period = info_in[-13:][0:9]
		final_contents[i].append(period)


#Drop identifiable data
for i in range(len(final_contents)):
	del final_contents[i][17]
	del final_contents[i][19]
	del final_contents[i][21]
	del final_contents[i][30]
	del final_contents[i][30]
	del final_contents[i][42]


#Write to output file
final_output_file = open(output_name, "w")
final_fileTotal = ""
for i in range(len(final_contents)):
	curr = final_contents[i]
	for j in range(len(curr)):
		final_fileTotal += curr[j]
		if(j!=len(curr)): final_fileTotal += "\t"
	if(i!=len(final_contents)): final_fileTotal += "\n"
final_output_file.writelines(final_fileTotal)
final_output_file.close()
print "File " + output_name + " was created."
























