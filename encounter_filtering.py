#Andrew Shen, 07/29/21
#Script to filter down output datasets from STARR, working with encounter data to keep only "completed, in-office encounters", then feed into "diagnosis_stats.py"
#To run: python encounter_filtering.py <path to encounters file> <path to diagnosis file> <path to master info file> <path to pt codebook file> encounter_filter_out.txt
#Ex: python encounter_filtering.py /Users/andrewshen/Desktop/encounters_medium.csv /Users/andrewshen/Desktop/diagnoses_medium.csv /Users/andrewshen/Desktop/master_info_medium.csv /Users/andrewshen/Desktop/pt_codebook_medium.csv encounter_filter_out.txt

#TODO
#1. (DONE) Count up the different types of "Visit Type"

import sys
import re

#Read in files
#sys.argv[1]: encounters file
#sys.argv[2]: diagnosis file
#sys.argv[3]: master info file
#sys.argv[4]: pt codebook
#sys.argv[5]: output file

encounters_in = sys.argv[1]
diagnosis_in = sys.argv[2]
info_in = sys.argv[3]
mrn_in = sys.argv[4]
output_name = sys.argv[5]

with open(encounters_in, 'r') as file:
	encounters_contents = file.readlines() #format: each item is a different line
for i in range(len(encounters_contents)):
	curr = encounters_contents[i]
	split_line = curr.strip() #get rid of \n
	split_line = split_line.split(",")
	encounters_contents[i] = split_line #format: each item composed of values separated by tabs

encounters_dict = {} #first values is number of encounters patient has had
for line in encounters_contents:
	if(encounters_dict.has_key(line[0])==False):
		encounters_dict[line[0]] = [1]
	else:
		encounters_dict[line[0]][0] = encounters_dict[line[0]][0]+1
#print encounters_dict.keys()
del(encounters_dict['"Patient Id"'])

encounters_count = 0
for key in encounters_dict.keys():
	if(encounters_dict[key][0]!=0):
		encounters_count = encounters_count + 1
	#print key
print "Number of patients is: " + str(encounters_count)
print

with open(diagnosis_in, 'r') as file:
	diagnosis_contents = file.readlines() #format: each item is a different line
for i in range(len(diagnosis_contents)):
	curr = diagnosis_contents[i]
	split_line = curr.strip() #get rid of \n
	#split_line = split_line.split(",")
	result = re.split(r"\",|,\"", split_line)
	diagnosis_contents[i] = result
	#diagnosis_contents[i] = split_line #format: each item composed of values separated by tabs

#for line in diagnosis_contents:
	#print len(line)
#	print line

for i in range(len(diagnosis_contents)):
	curr = diagnosis_contents[i]
	for j in range(len(curr)):
		if(curr[j]=="" or curr[j]=='"'): diagnosis_contents[i][j] = "blank"
		else: diagnosis_contents[i][j] = curr[j].replace('"', '')

#print diagnosis_contents[0]
#print len(diagnosis_contents[0])
#print diagnosis_contents[1]
#print len(diagnosis_contents[1])

#for line in diagnosis_contents:
	#print len(line)
#	print line
#print

with open(info_in, 'r') as file:
	info_contents = file.readlines() #format: each item is a different line
for i in range(len(info_contents)):
	curr = info_contents[i]
	split_line = curr.strip() #get rid of \n
	split_line = split_line.split(",")
	info_contents[i] = split_line #format: each item composed of values separated by tabs

with open(mrn_in, 'r') as file:
	mrn_contents = file.readlines() #format: each item is a different line
for i in range(len(mrn_contents)):
	curr = mrn_contents[i]
	split_line = curr.strip() #get rid of \n
	split_line = split_line.split(",")
	mrn_contents[i] = split_line #format: each item composed of values separated by tabs

#for line in mrn_contents:
#	print line[1]



#Do frequency analysis for the "appt type"
apptTypes_dict = {}
for i in range(len(encounters_contents)):
	curr = encounters_contents[i]
	currApptType = curr[3]
	if(currApptType not in apptTypes_dict): apptTypes_dict[currApptType] = 1
	else: apptTypes_dict[currApptType] = apptTypes_dict[currApptType] + 1
#for k,v in apptTypes_dict.iteritems():
#	print "%s: %d" % (k,v)

#Filter for "Encounter Type" (E: Office Visit), "Appt Status" (P: completed)
#Then work with "Visit Type" (Q)

out1_file = open("out1.txt", "w") #all encounters that have designation "Office Visit"
out2_file = open("out2.txt", "w") #all encounters with designation "Office Visit" and "Completed"
out3_file = open("out3.txt", "w") #all encounters with designation "Office Visit", "Completed", and relevant "VISIT TYPE"

#for File 1
#Write to output file
out1_contents = ""
for i in range(len(encounters_contents)):
	curr = encounters_contents[i]
	if(i==0): #populate the headers for the file
		for j in range(len(curr)):
			out1_contents += curr[j]
			out1_contents += "\t"
		out1_contents += "\n"
	#print curr[14]
	if(curr[14]=='"Ophthalmology"'):
		if(curr[4]=='"Office Visit"' or curr[4]=='"Telemedicine"' or curr[4]=='"Telemedicine Visit-Phone"'):
			#print curr
			for j in range(len(curr)):
				out1_contents += curr[j]
				if(j!=len(curr)): out1_contents += "\t"
			if(i!=len(encounters_contents)): out1_contents += "\n"
out1_file.writelines(out1_contents)
out1_file.close()
print "File 'out1.txt' was created."

#Create dictionary to count up stats
out1_dict = {} #first values is number of entries with "Office Visit"
out1_contents = out1_contents.splitlines()
for i in range(len(out1_contents)):
	curr = out1_contents[i]
	split_line = curr.strip() #get rid of \n
	split_line = split_line.split("\t")
	out1_contents[i] = split_line
for line in encounters_contents:
	out1_dict[line[0]] = [0]
for line in out1_contents:
	out1_dict[line[0]][0] = out1_dict[line[0]][0]+1
del(out1_dict['"Patient Id"'])

out1count = 0
for key in out1_dict.keys():
	if(out1_dict[key][0]!=0):
		out1count = out1count + 1
	#print key
print "Number of patients with 'Office Visit' is: " + str(out1count)
print

#for File 2
out2_contents = ""
for i in range(len(out1_contents)):
	curr = out1_contents[i]
	if(i==0): #populate the headers for the file
		for j in range(len(curr)):
			out2_contents += curr[j]
			out2_contents += "\t"
		out2_contents += "\n"
	if(curr[15]=='"Completed"'):
		#print curr
		for j in range(len(curr)):
			out2_contents += curr[j]
			if(j!=len(curr)): out2_contents += "\t"
		if(i!=len(out1_contents)): out2_contents += "\n"
out2_file.writelines(out2_contents)
out2_file.close()
print "File 'out2.txt' was created."

out2_dict = {} #first values is number of entries with "Office Visit"
out2_contents = out2_contents.splitlines()
for i in range(len(out2_contents)):
	curr = out2_contents[i]
	split_line = curr.strip() #get rid of \n
	split_line = split_line.split("\t")
	out2_contents[i] = split_line
for line in encounters_contents:
	out2_dict[line[0]] = [0]
for line in out2_contents:
	out2_dict[line[0]][0] = out2_dict[line[0]][0]+1
del(out2_dict['"Patient Id"'])

out2count = 0
for key in out2_dict.keys():
	if(out2_dict[key][0]!=0):
		out2count = out2count + 1
	#print key
print "Number of patients with 'Office Visit' and 'Completed' is: " + str(out2count)
print





#Filtering by Visit Type
visitTypes_dict = {}
for line in out2_contents:
	edited = line[16].strip('\"')
	edited = edited.strip()
	line[16] = edited
	#print line[16]
	if(visitTypes_dict.has_key(line[16])==False):
		visitTypes_dict[line[16]] = [1]
	else:
		visitTypes_dict[line[16]][0] = visitTypes_dict[line[16]][0]+1
del visitTypes_dict["Visit Type"]
#print "Visit Types All"
#for k,v in visitTypes_dict.items():
#	print str(k) + ": " + str(v)


#for line in out2_contents:
	#print line
#	print len(line)


visitTypes_dict_filtered = {}
for i in range(len(out2_contents)):
	#print line[16]
	edited_visitType = out2_contents[i][16].split(" ")
	#print edited_visitType[1]
	#print line[16][0:8]
	#print line[16][-6:]
#Replace the "Visit Type" with the more general filtered ones
	if(len(edited_visitType)>1 and edited_visitType[1] == "PATIENT"):
		if(visitTypes_dict_filtered.has_key("NEW/RETURN PATIENT")==False):
			visitTypes_dict_filtered["NEW/RETURN PATIENT"] = [1]
		else: 
			visitTypes_dict_filtered["NEW/RETURN PATIENT"][0] = visitTypes_dict_filtered["NEW/RETURN PATIENT"][0] + 1
		out2_contents[i].append("NEW/RETURN PATIENT")
		#print out2_contents[i]
	elif(len(out2_contents[i][16])>9 and out2_contents[i][16][0:9]=="INJECTION"):
		if(visitTypes_dict_filtered.has_key("INJECTIONS")==False):
			visitTypes_dict_filtered["INJECTIONS"] = [1]
		else: 
			visitTypes_dict_filtered["INJECTIONS"][0] = visitTypes_dict_filtered["INJECTIONS"][0] + 1
		out2_contents[i].append("INJECTIONS")
	elif(len(edited_visitType)==3 and edited_visitType[2] == "FIELD"):
		if(visitTypes_dict_filtered.has_key("VISUAL FIELD")==False):
			visitTypes_dict_filtered["VISUAL FIELD"] = [1]
		else: 
			visitTypes_dict_filtered["VISUAL FIELD"][0] = visitTypes_dict_filtered["VISUAL FIELD"][0] + 1
		out2_contents[i].append("VISUAL FIELD")
	elif(out2_contents[i][16][0:4]=="POST" or out2_contents[i][16][0:3]=="PRE" or out2_contents[i][16][-6:]=="POSTOP"):
		if(visitTypes_dict_filtered.has_key("POST/PRE OP")==False):
			visitTypes_dict_filtered["POST/PRE OP"] = [1]
		else: 
			visitTypes_dict_filtered["POST/PRE OP"][0] = visitTypes_dict_filtered["POST/PRE OP"][0] + 1
		out2_contents[i].append("POST/PRE OP")
	#else:
	#	if(visitTypes_dict_filtered.has_key(out2_contents[i][16])==False):
	#		visitTypes_dict_filtered[out2_contents[i][16]] = [1]
	#	else:
	#		visitTypes_dict_filtered[out2_contents[i][16]][0] = visitTypes_dict_filtered[out2_contents[i][16]][0]+1
	else:
		if(out2_contents[i][16] == "Visit Type"): continue
		elif(visitTypes_dict_filtered.has_key("MISC")==False):
			visitTypes_dict_filtered["MISC"] = [1]
		else:
			visitTypes_dict_filtered["MISC"][0] = visitTypes_dict_filtered["MISC"][0]+1
		if(out2_contents[i][16] != "Visit Type"): out2_contents[i].append("MISC")
out2_contents[0].append("Generic Visit Type")
#for line in out2_contents:
	#print line
	#print len(line)
	#print line[25]
#del visitTypes_dict_filtered["Visit Type"]
#print "Visit Types Filtered"
#for k,v in visitTypes_dict_filtered.items():
#	print str(k) + ": " + str(v)

#for File 3
out3_contents = ""
for i in range(len(out2_contents)):
	curr = out2_contents[i]
	#print curr[23]
	if(i==0): #populate the headers for the file
		for j in range(len(curr)):
			out3_contents += curr[j]
			out3_contents += "\t"
		out3_contents += "\n"
	#elif(curr[25]=="NEW/RETURN PATIENT"):
	#keeping all types right now
		#print curr
	else:
		for j in range(len(curr)):
			out3_contents += curr[j]
			if(j!=len(curr)): out3_contents += "\t"
		if(i!=len(out2_contents)): out3_contents += "\n"
out3_file.writelines(out3_contents)
out3_file.close()
print "File 'out3.txt' was created."

#for i in range(len(out3_contents)):
#	if i>1: print line[25]

out3_dict = {} #first values is number of entries with "Office Visit"
out3_contents = out3_contents.splitlines()
for i in range(len(out3_contents)):
	curr = out3_contents[i]
	split_line = curr.strip() #get rid of \n
	split_line = split_line.split("\t")
	out3_contents[i] = split_line
for line in encounters_contents:
	out3_dict[line[0]] = [0]
for line in out3_contents:
	out3_dict[line[0]][0] = out3_dict[line[0]][0]+1
del(out3_dict['"Patient Id"'])

out3count = 0
for key in out3_dict.keys():
	if(out3_dict[key][0]!=0):
		out3count = out3count + 1
	#print key
print "Number of patients with 'Office Visit', 'Completed', and relevant 'VISIT TYPE': " + str(out3count)
print

#for i in range(len(diagnosis_contents)):
#	curr = diagnosis_contents[i][7]
#	print curr


#Match up with the diagnosis file, output an edited diagnosis file
#Include only patients who show up in out3_dict
diagnosis_out = open("diagnosis_medium_edited.txt", "w")
includedPatients = []
for key in out3_dict.keys():
	if(out3_dict[key][0]!=0):
		includedPatients.append(key.replace('"',''))
#print includedPatients
diagnosis_edited = ""
#print len(includedPatients)
for i in range(len(diagnosis_contents)):
	curr = diagnosis_contents[i]
	if(i==0): #populate the headers for the file
		for j in range(len(curr)):
			diagnosis_edited += curr[j]
			diagnosis_edited += "\t"
		diagnosis_edited += "\n"
	if(curr[0] in includedPatients):
		for j in range(len(curr)):
			diagnosis_edited += curr[j]
			if(j!=len(curr)): diagnosis_edited += "\t"
		if(i!=len(diagnosis_contents)): diagnosis_edited += "\n"
diagnosis_out.writelines(diagnosis_edited)
diagnosis_out.close()
print "File 'diagnosis_medium_edited.txt' was created."












