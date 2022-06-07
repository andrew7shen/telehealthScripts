#Andrew Shen, 07/07/21
#Script to perform basic analysis of distribution of diagnosis data for Stanford telehealth
#To run: python diagnosis_stats.py <path to master diagnosis file> <path to master info file> <name of output file>
#Ex: python diagnosis_stats.py /Users/andrewshen/Desktop/diagnoses_3.15-4.15_tsv.txt /Users/andrewshen/Desktop/master_info_tsv.txt stats_out.txt
#With input file in tsv format

#TODO
#1. (DONE) Add another input file (master info file) to match time-dependent IDs to master IDs
#2. (DONE) Figure out primary diagnoses
#3. (IGNORE) Finish print_dict method (to print out contents of dictionary in nice manner)
#4. (DONE) Edit how I populate temp_dict to include all of the items' and its G and I columns; number diagnoses, number primary diagnoses, item 1, item 2... (ALL included already, stats calculated from the excel file)
#5. (DONE) write to output file "stats_out.txt" to see the info about the input files

#IMPORTANT VARIABLES
#diagnosis_contents
#info_contents
#temp_dict

import sys
import re

#Read in files
#sys.argv[1]: master diagnosis file
#sys.argv[2]: master info file
diagnosis_in = sys.argv[1]
info_in = sys.argv[2]
output_name = sys.argv[3]

with open(diagnosis_in, 'r') as file:
	diagnosis_contents = file.readlines() #format: each item is a different line
hasPeriod = False
checkPeriod = diagnosis_contents[0][-8:].strip()
#print checkPeriod
if checkPeriod=="Period": hasPeriod = True
print "hasPeriod is: " + str(hasPeriod)
for i in range(len(diagnosis_contents)):
	curr = diagnosis_contents[i]
	split_line = curr.strip() #get rid of \n

	#print curr
#	if(hasPeriod == False):
#		result = re.split(r"\",|,\"", split_line)
#		split_line = result
		#diagnosis_contents[i] = result
		#print "Split by quotation marks"
	#else:
	#	split_line = split_line.split("\t")
	#	diagnosis_contents[i] = split_line #format: each item composed of values separated by tabs
	split_line = split_line.split("\t")
		#print "Split by tab"
	diagnosis_contents[i] = split_line
	
	#print curr
	#split_line = split_line.split("\"")
	#split_line = [line for line in [line.strip() for line in split_line.split("\"")] if line]

	#print split_line
	#print len(split_line)
	#split_line = split_line.split("\t")
	
if hasPeriod:
	diagnosis_contents[0].append("Master ID")
#print diagnosis_contents[0][0]

else:
	diagnoses_dict = {} #first values is number of diagnoses patient has had
	for line in diagnosis_contents:
		if(diagnoses_dict.has_key(line[0])==False):
			diagnoses_dict[line[0]] = [1]
		else:
			diagnoses_dict[line[0]][0] = diagnoses_dict[line[0]][0]+1



with open(info_in, 'r') as file:
	info_contents = file.readlines()
for i in range(len(info_contents)):
	curr = info_contents[i]
	split_line = curr.strip() #get rid of \n
	split_line = split_line.split("\t")
	info_contents[i] = split_line #format: each item composed of values separated by tabs




#print diagnosis_contents[1]

#Matches up IDs and writes out to file, if the file has period designation
if len(diagnosis_contents[1])>11:
	for i in range(len(diagnosis_contents)):
		curr_ID = diagnosis_contents[i][0]
		curr_period = diagnosis_contents[i][11] #if has period designation
		for j in range(len(info_contents)-1):
			if(len(info_contents[j])!=1):
				test_ID = info_contents[j][2]
				test_period = info_contents[j][1]
				if(curr_ID==test_ID and curr_period==test_period): #matches up time-dependent ID and master ID
					diagnosis_contents[i].append(info_contents[j][0])
					break
	ID_output_file = open("diagnoses_3.15-4.15_updatedID_tsv.txt", "w")
	#Assemble large string to write to ID_output_file
	ID_fileTotal = ""
	for i in range(len(diagnosis_contents)):
		curr = diagnosis_contents[i]
		for j in range(len(curr)):
			ID_fileTotal += curr[j]
			if(j!=len(curr)): ID_fileTotal += "\t"
		if(i!=len(diagnosis_contents)): ID_fileTotal += "\n"
	#Write to output file diagnoses_3.15-4.15_updatedID_tsv.txt
	ID_output_file.writelines(ID_fileTotal)
	ID_output_file.close()
	print "File 'diagnoses_3.15-4.15_updatedID_tsv.txt' was created."
else:
	print "File with updated IDs was not created."

if hasPeriod:
	diagnoses_dict = {} #first values is number of diagnoses patient has had
	for line in diagnosis_contents:
		if(len(line)>12):
			if(diagnoses_dict.has_key(line[12])==False):
				diagnoses_dict[line[12]] = [1]
			else:
				diagnoses_dict[line[12]][0] = diagnoses_dict[line[12]][0]+1






#Filtering: will have three output files
	#File 1: diagnoses_3.15-4.15_updatedID_1_tsv.txt
	#File 2: diagnoses_3.15-4.15_updatedID_12_tsv.txt
	#File 3: diagnoses_3.15-4.15_updatedID_123_tsv.txt
	#1: performing provider, 2: primary diagnosis, 3: professional billing code
out_1_file = open("out_1.txt", "w")
out_12_file = open("out_12.txt", "w")
out_12_3_file = open("out_12_3.txt", "w")
out_123_file = open("out_123.txt", "w")
#for File 1
out_1_fileContents = ""
for i in range(len(diagnosis_contents)):
	curr = diagnosis_contents[i]
	#print curr
	#print len(curr)
	if(i==0): #populate the headers for the file
		for j in range(len(curr)):
			out_1_fileContents += curr[j]
			out_1_fileContents += "\t"
		out_1_fileContents += "\n"
	if(len(curr[8])>1): #curr[8] is performing provider
		temp_provider = curr[8][1:-1]
		if(len(curr[8])>12):
			checkProvider = temp_provider[-13:]
			#print checkProvider
			if(checkProvider=="OPHTHALMOLOGY" or checkProvider==" OPHTHALMOLOG"): #issue with quotations
				for j in range(len(curr)):
					out_1_fileContents += curr[j]
					if(j!=len(curr)): out_1_fileContents += "\t"
				if(i!=len(diagnosis_contents)): out_1_fileContents += "\n"
#print out_1_fileContents
out_1_file.writelines(out_1_fileContents)
out_1_file.close()
print "File 'out_1.txt' was created."
#make temp dictionary for File 1 to count keys
file1_temp_dict = {} #first values is number of entries with OPTHALMOLOGY
out_1_fileContents = out_1_fileContents.splitlines()
for i in range(len(out_1_fileContents)):
	curr = out_1_fileContents[i]
	split_line = curr.strip() #get rid of \n
	split_line = split_line.split("\t")
	out_1_fileContents[i] = split_line
for line in diagnosis_contents: #use diagnosis_contents so contain all patients
	dict_value = [0]
	#print len(line)
	if(len(line)==13): file1_temp_dict[line[12]] = dict_value #has period
	elif(len(line)==11): file1_temp_dict[line[0]] = dict_value #has no period
#print file1_temp_dict.keys()
for line in out_1_fileContents:
	if(len(line)==13): file1_temp_dict[line[12]][0] = file1_temp_dict[line[12]][0]+1 #has period
	elif(len(line)==11): file1_temp_dict[line[0]][0] = file1_temp_dict[line[0]][0]+1 #no period
if "Master ID" in file1_temp_dict: del(file1_temp_dict["Master ID"])
elif "Patient Id" in file1_temp_dict: del(file1_temp_dict["Patient Id"])

#for File 2
out_12_fileContents = ""
for i in range(len(out_1_fileContents)):
	curr = out_1_fileContents[i]
	edit_primary = curr[3].strip()
	curr[3] = edit_primary
	if(i==0): #populate the headers for the file
		for j in range(len(curr)):
			out_12_fileContents += curr[j]
			out_12_fileContents += "\t"
		out_12_fileContents += "\n"
	if(len(curr)==13 or len(curr)==11):
		if(curr[3]=="Primary" or curr[3]=="Chronic" or curr[3]=="ED" or curr[3]=="Present on admission" or curr[3]=="Primary ED" or curr[3]=="Primary Chronic"):
			for j in range(len(curr)):
				out_12_fileContents += curr[j]
				if(j!=len(curr)): out_12_fileContents += "\t"
			if(i!=len(out_1_fileContents)): out_12_fileContents += "\n"

out_12_file.writelines(out_12_fileContents)
out_12_file.close()
print "File 'out_12.txt' was created."
#make temp dictionary for File 2 to count keys
file12_temp_dict = {} #first values is number of entries with OPTHALMOLOGY and PRIMARY
out_12_fileContents = out_12_fileContents.splitlines()
for i in range(len(out_12_fileContents)):
	curr = out_12_fileContents[i]
	split_line = curr.strip() #get rid of \n
	split_line = split_line.split("\t")
	out_12_fileContents[i] = split_line
for line in diagnosis_contents:
	dict_value = [0]
	if(len(line)==13): file12_temp_dict[line[12]] = dict_value #has period
	elif(len(line)==11): file12_temp_dict[line[0]] = dict_value #has no period
for line in out_12_fileContents:
	if(len(line)==13): file12_temp_dict[line[12]][0] = file12_temp_dict[line[12]][0]+1 #has period
	elif(len(line)==11): file12_temp_dict[line[0]][0] = file12_temp_dict[line[0]][0]+1 #has no period
if "Master ID" in file12_temp_dict: del(file12_temp_dict["Master ID"])
elif "Patient Id" in file12_temp_dict: del(file12_temp_dict["Patient Id"])


#for opth/primary without professional billing code
out_12_3_fileContents = ""
for i in range(len(out_12_fileContents)):
	curr = out_12_fileContents[i]
	edit_billing = curr[4].strip()
	curr[4] = edit_billing
	if(len(curr)==13 or len(curr)==11):
		if(curr[4]!="Professional Billing Code"):
			for j in range(len(curr)):
				out_12_3_fileContents += curr[j]
				if(j!=len(curr)): out_12_3_fileContents += "\t"
			if(i!=len(out_12_fileContents)): out_12_3_fileContents += "\n"

out_12_3_file.writelines(out_12_3_fileContents)
out_12_3_file.close()
print "File 'out_12_3.txt' was created."
#make temp dictionary for File 3 to count keys
file12_3_temp_dict = {}
out_12_3_fileContents = out_12_3_fileContents.splitlines()
for i in range(len(out_12_3_fileContents)):
	curr = out_12_3_fileContents[i]
	split_line = curr.strip() #get rid of \n
	split_line = split_line.split("\t")
	out_12_3_fileContents[i] = split_line
for line in diagnosis_contents:
	dict_value = [0]
	if(len(line)==13): file12_3_temp_dict[line[12]] = dict_value #has period
	elif(len(line)==11): file12_3_temp_dict[line[0]] = dict_value #has no period
for line in out_12_3_fileContents:
	if(len(line)==13): file12_3_temp_dict[line[12]][0] = file12_3_temp_dict[line[12]][0]+1 #has period
	elif(len(line)==11): file12_3_temp_dict[line[0]][0] = file12_3_temp_dict[line[0]][0]+1 #has no period
if "Master ID" in file12_3_temp_dict: del(file12_3_temp_dict["Master ID"])
elif "Patient Id" in file12_3_temp_dict: del(file12_3_temp_dict["Patient Id"])


#for opth without professional billing code
#Try to solve loss of 5 patients: working with out_1_fileContents rather than out_2_fileContents
out_1_3_file = open("out_1_3.txt", "w")
#for opth/primary without professional billing code
out_1_3_fileContents = ""
#print len(out_1_fileContents)
for i in range(len(out_1_fileContents)):
	curr = out_1_fileContents[i]
	edit_billing = curr[4].strip()
	curr[4] = edit_billing
	if(len(curr)==13 or len(curr)==11):
		if(curr[4]!="Professional Billing Code"):
			for j in range(len(curr)):
				out_1_3_fileContents += curr[j]
				if(j!=len(curr)): out_1_3_fileContents += "\t"
			if(i!=len(out_1_fileContents)): out_1_3_fileContents += "\n"

out_1_3_file.writelines(out_1_3_fileContents)
out_1_3_file.close()
print "File 'out_1_3.txt' was created."
#make temp dictionary for File 3 to count keys
file1_3_temp_dict = {}
out_1_3_fileContents = out_1_3_fileContents.splitlines()
for i in range(len(out_1_3_fileContents)):
	curr = out_1_3_fileContents[i]
	split_line = curr.strip() #get rid of \n
	split_line = split_line.split("\t")
	out_1_3_fileContents[i] = split_line
for line in diagnosis_contents:
	dict_value = [0]
	if(len(line)==13): file1_3_temp_dict[line[12]] = dict_value #has period
	elif(len(line)==11): file1_3_temp_dict[line[0]] = dict_value #has no period
for line in out_1_3_fileContents:
	if(len(line)==13): file1_3_temp_dict[line[12]][0] = file1_3_temp_dict[line[12]][0]+1 #has period
	elif(len(line)==11): file1_3_temp_dict[line[0]][0] = file1_3_temp_dict[line[0]][0]+1 #has no period
if "Master ID" in file1_3_temp_dict: del(file1_3_temp_dict["Master ID"])
elif "Patient Id" in file1_3_temp_dict: del(file1_3_temp_dict["Patient Id"])


#for opth without professional billing code then drop non-primary unless if not the only one
out_1_3_2_file = open("out_1_3_2.txt", "w")
#for opth/primary without professional billing code
addedValues = []
out_1_3_2_fileContents = ""
#print len(out_1_3_fileContents)
for i in range(len(out_1_3_fileContents)):
	curr = out_1_3_fileContents[i]
	edit_billing = curr[4].strip()
	curr[4] = edit_billing
	#print len(curr)
	if(len(curr)==13 or len(curr)==11):
		#print "yes"
		if(curr[0]=="Patient Id"):
			for j in range(len(curr)):
				out_1_3_2_fileContents += curr[j]
				if(j!=len(curr)): out_1_3_2_fileContents += "\t"
			if(i!=len(out_1_fileContents)): out_1_3_2_fileContents += "\n"
		elif(curr[3]=="Primary"):
			if curr[0] not in addedValues:
				addedValues.append(curr[0])
				for j in range(len(curr)):
					out_1_3_2_fileContents += curr[j]
					if(j!=len(curr)): out_1_3_2_fileContents += "\t"
				if(i!=len(out_1_fileContents)): out_1_3_2_fileContents += "\n"
		else:
			#Check if there are any primaries, if not take the first one
			if curr[0] not in addedValues:
				checkID = curr[0]
				hasPrimary = False
				for k in range(len(out_1_3_fileContents)):
					curr1 = out_1_3_fileContents[k]
					if(curr1[0]==checkID and curr1[3]=="Primary"):
						hasPrimary = True
				if(hasPrimary==False): #if no primaries
					addedValues.append(curr[0])
					for j in range(len(curr)):
						out_1_3_2_fileContents += curr[j]
						if(j!=len(curr)): out_1_3_2_fileContents += "\t"
					if(i!=len(out_1_fileContents)): out_1_3_2_fileContents += "\n"

out_1_3_2_file.writelines(out_1_3_2_fileContents)
out_1_3_2_file.close()
print "File 'out_1_3_2.txt' was created."
#make temp dictionary for File 3 to count keys
file1_3_2_temp_dict = {}
out_1_3_2_fileContents = out_1_3_2_fileContents.splitlines()
for i in range(len(out_1_3_2_fileContents)):
	curr = out_1_3_2_fileContents[i]
	split_line = curr.strip() #get rid of \n
	split_line = split_line.split("\t")
	out_1_3_2_fileContents[i] = split_line
for line in diagnosis_contents:
	dict_value = [0]
	if(len(line)==13): file1_3_2_temp_dict[line[12]] = dict_value #has period
	elif(len(line)==11): file1_3_2_temp_dict[line[0]] = dict_value #has no period
for line in out_1_3_2_fileContents:
	if(len(line)==13): file1_3_2_temp_dict[line[12]][0] = file1_3_2_temp_dict[line[12]][0]+1 #has period
	elif(len(line)==11): file1_3_2_temp_dict[line[0]][0] = file1_3_2_temp_dict[line[0]][0]+1 #has no period
if "Master ID" in file1_3_2_temp_dict: del(file1_3_2_temp_dict["Master ID"])
elif "Patient Id" in file1_3_2_temp_dict: del(file1_3_2_temp_dict["Patient Id"])


#for File 3
out_123_fileContents = ""
for i in range(len(out_12_fileContents)):
	curr = out_12_fileContents[i]
	edit_billing = curr[4].strip()
	curr[4] = edit_billing
	if(i==0): #populate the headers for the file
		for j in range(len(curr)):
			out_123_fileContents += curr[j]
			out_123_fileContents += "\t"
		out_123_fileContents += "\n"
	if(len(curr)==13 or len(curr)==11):
		if(curr[4]=="Professional Billing Code"):
			for j in range(len(curr)):
				out_123_fileContents += curr[j]
				if(j!=len(curr)): out_123_fileContents += "\t"
			if(i!=len(out_12_fileContents)): out_123_fileContents += "\n"

out_123_file.writelines(out_123_fileContents)
out_123_file.close()
print "File 'out_123.txt' was created."
#make temp dictionary for File 3 to count keys
file123_temp_dict = {} #first values is number of entries with OPTHALMOLOGY, PRIMARY, and PROFESSIONAL BILLING CODE
out_123_fileContents = out_123_fileContents.splitlines()
for i in range(len(out_123_fileContents)):
	curr = out_123_fileContents[i]
	split_line = curr.strip() #get rid of \n
	split_line = split_line.split("\t")
	out_123_fileContents[i] = split_line
for line in diagnosis_contents:
	dict_value = [0]
	if(len(line)==13): file123_temp_dict[line[12]] = dict_value #has period
	elif(len(line)==11): file123_temp_dict[line[0]] = dict_value #has no period
for line in out_123_fileContents:
	if(len(line)==13): file123_temp_dict[line[12]][0] = file123_temp_dict[line[12]][0]+1 #has period
	elif(len(line)==11): file123_temp_dict[line[0]][0] = file123_temp_dict[line[0]][0]+1 #has no period
if "Master ID" in file123_temp_dict: del(file123_temp_dict["Master ID"])
elif "Patient Id" in file123_temp_dict: del(file123_temp_dict["Patient Id"])






#For each patient ID, calculate ...
	#1. number of diagnoses
	#2. number of primary diagnoses
temp_dict = {} #key will be patient ID and will have two values
#calculate number of diagnoses
not_included = 0
for line in diagnosis_contents:
	edit_primary = line[3].strip()
	line[3] = edit_primary
	dict_value = [1,0] #first value is number of diagnoses, second value is number of primary diagnoses
	if(len(line)==13): #doesn't include values that don't have master IDs, #period
		if(temp_dict.has_key(line[12])==False):
			temp_dict[line[12]] = dict_value
		else:
			temp_dict[line[12]][0] = temp_dict[line[12]][0]+1
	else:
		not_included = not_included+1

	if(len(line)==11): #no period
		if(temp_dict.has_key(0)==False):
			temp_dict[line[0]] = dict_value
		else:
			temp_dict[line[0]][0] = temp_dict[line[0]][0]+1
	else:
		not_included = not_included+1
if "Master ID" in temp_dict: del(temp_dict["Master ID"])
elif "Patient Id" in temp_dict: del(temp_dict["Patient Id"])

#calculate number of primary diagnoses
for line in diagnosis_contents:
	if(len(line)==13):
		if(line[3]=="Primary" or line[3]=="Chronic" or line[3]=="ED" or line[3]=="Present on admission" or line[3]=="Primary ED" or line[3]=="Primary Chronic"):
			temp_dict[line[12]][1] = temp_dict[line[12]][1]+1
	
	if(len(line)==11):
		if(line[3]=="Primary" or line[3]=="Chronic" or line[3]=="ED" or line[3]=="Present on admission" or line[3]=="Primary ED" or line[3]=="Primary Chronic"):
			temp_dict[line[0]][1] = temp_dict[line[0]][1]+1







#print_dict method: easy way to visualize calculated statistics about the information
def print_dict(dictionary):
	print "Number of dictionary keys: " + str(len(dictionary.keys()))







#Write to output file stats_out.txt
final_output_file = open(output_name, "w")
final_fileTotal = "ID_overall\tNumber of Diagnoses\tNumber of Primary Diagnoses\n"
total_entries = 0
for entry in temp_dict.keys():
	curr = temp_dict[entry]
	total_entries+=curr[0]
	createdString = entry + "\t" + str(curr[0]) + "\t" + str(curr[1]) + "\n"
	final_fileTotal = final_fileTotal + createdString
final_output_file.writelines(final_fileTotal)
final_output_file.close()
print "File " + output_name + " was created."
print



if "Master ID" in diagnoses_dict: del(diagnoses_dict["Master ID"])
elif "Patient Id" in diagnoses_dict: del(diagnoses_dict["Patient Id"])
print "Number of unique patients: " + str(len(diagnoses_dict.keys()))

#CHECK: Opthalmology filter
#print_dict(file1_temp_dict)
allCount = 0
for key in file1_temp_dict.keys():
	if(file1_temp_dict[key][0]!=0):
		allCount = allCount +1
		#print key
print "Number of unique patients under OPTHALMOLOGY: " + str(allCount)

#CHECK: Primary filter
#print_dict(file12_temp_dict)
allCount = 0
for key in file12_temp_dict.keys():
	if(file12_temp_dict[key][0]!=0):
		allCount = allCount +1
		#print key
#print
print  "Number of unique patients under OPTHALMOLOGY and PRIMARY: " + str(allCount)

#CHECK: Source filter
#print_dict(file123_temp_dict)
allCount = 0
for key in file123_temp_dict.keys():
	if(file123_temp_dict[key][0]!=0):
		allCount = allCount +1
		#print key
#print
print  "Number of unique patients under OPTHALMOLOGY and PRIMARY and PROFESSIONAL BILLING CODE: " + str(allCount)

#CHECK: opth/primary without professional billing code filter
#print_dict(file12_temp_dict)
allCount = 0
for key in file12_3_temp_dict.keys():
	if(file12_3_temp_dict[key][0]!=0):
		allCount = allCount +1
		#print key
#print
print  "Number of unique patients under OPTHALMOLOGY and PRIMARY without PROFESSIONAL BILLING CODE: " + str(allCount)

#CHECK: opth without professional billing code filter
#print_dict(file12_temp_dict)
allCount = 0
for key in file1_3_temp_dict.keys():
	if(file1_3_temp_dict[key][0]!=0):
		allCount = allCount +1
		#print key
#print
print  "Number of unique patients under OPTHALMOLOGY without PROFESSIONAL BILLING CODE: " + str(allCount)

#CHECK: opth without professional billing code filter then drop primary if not only one
#print_dict(file12_temp_dict)
allCount = 0
for key in file1_3_2_temp_dict.keys():
	if(file1_3_2_temp_dict[key][0]!=0):
		allCount = allCount +1
		#print key
#print
print  "Number of unique patients under OPTHALMOLOGY without PROFESSIONAL BILLING CODE and with PRIMARY unless no primaries: " + str(allCount)


#Check difference between dict_12 and dict_12_3
#for key in file12_temp_dict.keys():
#	if (file12_temp_dict[key][0]!=0 and file12_3_temp_dict[key][0]==0):
#		print key

#Check difference between dict_1 and dict_1_3
#for key in file1_temp_dict.keys():
#	if (file1_temp_dict[key][0]!=0 and file1_3_temp_dict[key][0]==0):
#		print key

#Check difference between dict_1/dict_1_3 and dict_1_3_2
for key in file1_3_temp_dict.keys():
	if (file1_3_temp_dict[key][0]!=0 and file1_3_2_temp_dict[key][0]==0):
		print key

#print file1_temp_dict["2"]
#print file1_temp_dict["42"]
#print file1_temp_dict["57"]
#print file1_temp_dict

#print "Number of dictionary keys: " + str(len(temp_dict.keys()))
#print "Number of entries/lines missing masterID: " + str(not_included)
#print "Total number of entries: " + str(total_entries) + "(should be 21649-" + str(not_included) + "=" + str(21649-not_included) + ")"
#print_dict()
#print temp_dict.keys()
#print len(temp_dict.keys())
#print temp_dict["1"]
#print temp_dict["2"]
#print temp_dict["3"]
#print temp_dict["100"]
#print diagnosis_contents[0]