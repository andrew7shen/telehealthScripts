#Andrew Shen, 09/07/21
#Script to assign masterIDs to the final masterTable created from overlapping cohorts
#To run: python matchIDs.py <path to masterTable file> <path to master patient info file 1> <path to master patient info file 2> <name of output file>
#Ex: python matchIDs.py /Users/andrewshen/Desktop/masterTable_overlap.txt /Users/andrewshen/Desktop/patientCodebook_overlap_3.16-3.17.csv /Users/andrewshen/Desktop/patientCodebook_overlap_3.17-3.18.csv masterTable_overlap_final.txt

#NOTE: not entirely automated, not code to take in varying input lengths, need to edit when changing number of inputs
#		currently set for tele2021 runs

import sys
import re
import operator

masterTable_in = sys.argv[1]
info1_in = sys.argv[2]
info2_in = sys.argv[3]
info3_in = sys.argv[4]
info4_in = sys.argv[5]
info5_in = sys.argv[6]
info6_in = sys.argv[7]
info7_in = sys.argv[8]
output_name = sys.argv[9]
#output_name = sys.argv[7]

#Read in input files
with open(masterTable_in, 'r') as file:
	masterTable_contents = file.readlines() #format: each item is a different line
for i in range(len(masterTable_contents)):
	curr = masterTable_contents[i]
	split_line = curr.strip() #get rid of \n
	split_line = split_line.split("\t")
	masterTable_contents[i] = split_line #format: each item composed of values separated by tabs

with open(info1_in, 'r') as file:
	info1_contents = file.readlines() #format: each item is a different line
for i in range(len(info1_contents)):
	curr = info1_contents[i]
	split_line = curr.strip() #get rid of \n
	result = re.split(r'(?<![A-Z]),', split_line, flags=re.I)
	info1_contents[i] = result
period1 = info1_in[-13:][0:9]

with open(info2_in, 'r') as file:
	info2_contents = file.readlines() #format: each item is a different line
for i in range(len(info2_contents)):
	curr = info2_contents[i]
	split_line = curr.strip() #get rid of \n
	result = re.split(r'(?<![A-Z]),', split_line, flags=re.I)
	info2_contents[i] = result
period2 = info2_in[-13:][0:9]

with open(info3_in, 'r') as file:
	info3_contents = file.readlines() #format: each item is a different line
for i in range(len(info3_contents)):
	curr = info3_contents[i]
	split_line = curr.strip() #get rid of \n
	result = re.split(r'(?<![A-Z]),', split_line, flags=re.I)
	info3_contents[i] = result
period3 = info3_in[-13:][0:9]

with open(info4_in, 'r') as file:
	info4_contents = file.readlines() #format: each item is a different line
for i in range(len(info4_contents)):
	curr = info4_contents[i]
	split_line = curr.strip() #get rid of \n
	result = re.split(r'(?<![A-Z]),', split_line, flags=re.I)
	info4_contents[i] = result
period4 = info4_in[-13:][0:9]

with open(info5_in, 'r') as file:
	info5_contents = file.readlines() #format: each item is a different line
for i in range(len(info5_contents)):
	curr = info5_contents[i]
	split_line = curr.strip() #get rid of \n
	result = re.split(r'(?<![A-Z]),', split_line, flags=re.I)
	info5_contents[i] = result
period5 = info5_in[-13:][0:9]

with open(info6_in, 'r') as file:
	info6_contents = file.readlines() #format: each item is a different line
for i in range(len(info6_contents)):
	curr = info6_contents[i]
	split_line = curr.strip() #get rid of \n
	result = re.split(r'(?<![A-Z]),', split_line, flags=re.I)
	info6_contents[i] = result
period6 = info6_in[-13:][0:9]

with open(info7_in, 'r') as file:
	info7_contents = file.readlines() #format: each item is a different line
for i in range(len(info7_contents)):
	curr = info7_contents[i]
	split_line = curr.strip() #get rid of \n
	result = re.split(r'(?<![A-Z]),', split_line, flags=re.I)
	info7_contents[i] = result
period7 = info7_in[-13:][0:9]


#Add MRNs, added in if MRN not found
final_contents = masterTable_contents
final_contents[0].append("MRN")
for i in range(len(masterTable_contents)):
	#print i
	#print masterTable_contents[i]
	currPeriod = masterTable_contents[i][50]
	#print currPeriod
	currID = masterTable_contents[i][0]
	mrnFound = False
	if(currPeriod == period1):
		for j in range(len(info1_contents)):
			infoID = info1_contents[j][0].replace('"', '')
			infoMRN = info1_contents[j][1]
			if(infoID == currID): 
				final_contents[i].append(infoMRN)
				mrnFound = True
		if(mrnFound == False): final_contents[i].append("noMRN")	
	elif(currPeriod == period2):
		for j in range(len(info2_contents)):
			infoID = info2_contents[j][0].replace('"', '')
			infoMRN = info2_contents[j][1]
			if(infoID == currID):
				final_contents[i].append(infoMRN)
				mrnFound = True
		if(mrnFound == False): final_contents[i].append("noMRN")
	elif(currPeriod == period3):
		for j in range(len(info3_contents)):
			infoID = info3_contents[j][0].replace('"', '')
			infoMRN = info3_contents[j][1]
			if(infoID == currID):
				final_contents[i].append(infoMRN)
				mrnFound = True
		if(mrnFound == False): final_contents[i].append("noMRN")
	elif(currPeriod == period4):
		for j in range(len(info4_contents)):
			infoID = info4_contents[j][0].replace('"', '')
			infoMRN = info4_contents[j][1]
			if(infoID == currID):
				final_contents[i].append(infoMRN)
				mrnFound = True
		if(mrnFound == False): final_contents[i].append("noMRN")
	elif(currPeriod == period5):
		for j in range(len(info5_contents)):
			infoID = info5_contents[j][0].replace('"', '')
			infoMRN = info5_contents[j][1]
			if(infoID == currID):
				final_contents[i].append(infoMRN)
				mrnFound = True
		if(mrnFound == False): final_contents[i].append("noMRN")
	elif(currPeriod == period6):
		for j in range(len(info6_contents)):
			infoID = info6_contents[j][0].replace('"', '')
			infoMRN = info6_contents[j][1]
			if(infoID == currID):
				final_contents[i].append(infoMRN)
				mrnFound = True
		if(mrnFound == False): final_contents[i].append("noMRN")
	elif(currPeriod == period7):
		for j in range(len(info7_contents)):
			infoID = info7_contents[j][0].replace('"', '')
			infoMRN = info7_contents[j][1]
			if(infoID == currID):
				final_contents[i].append(infoMRN)
				mrnFound = True
		if(mrnFound == False): final_contents[i].append("noMRN")



#Add masterIDs
final_contents[0].append("masterID")
MRN_dict = {}
MRN_counter = 1
for i in range(1,len(final_contents)):
	currMRN = final_contents[i][51]
	if(currMRN not in MRN_dict):
		MRN_dict[currMRN] = MRN_counter
		MRN_counter = MRN_counter + 1
for i in range(1,len(final_contents)):
	currMRN = final_contents[i][51]
	newID = MRN_dict[currMRN]
	final_contents[i].append(str(newID))
#Delete MRN column
for i in range(len(final_contents)):
	del final_contents[i][51]

#Make dictionary to count up number of entries per patient
stats_dict = {}
for i in range(1,len(final_contents)):
	currMasterID = final_contents[i][51]
	#print currMasterID
	if(currMasterID not in stats_dict): stats_dict[currMasterID] = 1
	else: stats_dict[currMasterID] = stats_dict[currMasterID] + 1
counter_dict = {} #counts distribution of stats_dict
for k,v in stats_dict.iteritems():
	#print "k: %s, v: %d" % (k,v)
	if(v not in counter_dict): counter_dict[v] = 1
	else: counter_dict[v] = counter_dict[v] + 1
#for k,v in counter_dict.iteritems():
#	print "k: %s, v: %d" % (k,v)

#Add counter1: help cut down to one entry each per patient
final_contents[0].append("counter1")
checker1_dict = {}
for i in range(1,len(final_contents)):
	curr = final_contents[i]
	currID = curr[51] ###need to change after run through the new pipeline
	if currID not in checker1_dict:
		checker1_dict[currID] = 1
		final_contents[i].append(1)
	else:
		checker1_dict[currID] = checker1_dict[currID] + 1
		final_contents[i].append(checker1_dict[currID])

#Get distributions for the 6 different categories: visit type, appt type, performing provider, insurance, language, race/ethnicity
visitType_dict = {}
for i in range (1,len(final_contents)):
	curr = final_contents[i]
	currVisitType = curr[16]
	if(currVisitType not in visitType_dict): visitType_dict[currVisitType] = 1
	else: visitType_dict[currVisitType] = visitType_dict[currVisitType] + 1
apptType_dict = {}
for i in range (1,len(final_contents)):
	curr = final_contents[i]
	currApptType = curr[3]
	if(currApptType not in apptType_dict): apptType_dict[currApptType] = 1
	else: apptType_dict[currApptType] = apptType_dict[currApptType] + 1
provider_dict = {}
for i in range (1,len(final_contents)):
	curr = final_contents[i]
	currProvider = curr[27]
	if(currProvider not in provider_dict): provider_dict[currProvider] = 1
	else: provider_dict[currProvider] = provider_dict[currProvider] + 1
insurance_dict = {}
for i in range (1,len(final_contents)):
	curr = final_contents[i]
	currInsurance = curr[40]
	if(currInsurance not in insurance_dict): insurance_dict[currInsurance] = 1
	else: insurance_dict[currInsurance] = insurance_dict[currInsurance] + 1
language_dict = {}
for i in range (1,len(final_contents)):
	curr = final_contents[i]
	currLanguage = curr[37]
	if(currLanguage not in language_dict): language_dict[currLanguage] = 1
	else: language_dict[currLanguage] = language_dict[currLanguage] + 1
race_dict = {}
for i in range (1,len(final_contents)):
	curr = final_contents[i]
	currRace = curr[30]
	if(currRace not in race_dict): race_dict[currRace] = 1
	else: race_dict[currRace] = race_dict[currRace] + 1
ethnicity_dict = {}
for i in range (1,len(final_contents)):
	curr = final_contents[i]
	currEthnicity = curr[31]
	if(currEthnicity not in ethnicity_dict): ethnicity_dict[currEthnicity] = 1
	else: ethnicity_dict[currEthnicity] = ethnicity_dict[currEthnicity] + 1
#visitType_sorted_dict = sorted(visitType_dict.items(), key=operator.itemgetter(1), reverse=True)
#for k,v in visitType_sorted_dict:
#	print "%s: %d" % (k,v)
#apptType_sorted_dict = sorted(apptType_dict.items(), key=operator.itemgetter(1), reverse=True)
#for k,v in apptType_sorted_dict:
#	print "%s: %d" % (k,v)
#provider_sorted_dict = sorted(provider_dict.items(), key=operator.itemgetter(1), reverse=True)
#for k,v in provider_sorted_dict:
#	print "%s: %d" % (k,v)
#insurance_sorted_dict = sorted(insurance_dict.items(), key=operator.itemgetter(1), reverse=True)
#for k,v in insurance_sorted_dict:
#	print "%s: %d" % (k,v)
#language_sorted_dict = sorted(language_dict.items(), key=operator.itemgetter(1), reverse=True)
#for k,v in language_sorted_dict:
#	print "%s: %d" % (k,v)
#race_sorted_dict = sorted(race_dict.items(), key=operator.itemgetter(1), reverse=True)
#for k,v in race_sorted_dict:
#	print "%s: %d" % (k,v)
#ethnicity_sorted_dict = sorted(ethnicity_dict.items(), key=operator.itemgetter(1), reverse=True)
#for k,v in ethnicity_sorted_dict:
#	print "%s: %d" % (k,v)

#Add recoded distributions for variables
final_contents[0].insert(17, "type_collapsed")
final_contents[0].insert(18, "new_return")
final_contents[0].insert(19, "tele_or_not")
final_contents[0].insert(31, "service")
final_contents[0].insert(35, "race_coll")
final_contents[0].insert(43, "language_coll")
final_contents[0].insert(47, "insurance_coll")
for i in range(1,len(final_contents)):
	curr = final_contents[i]
	#Visit type
	if(curr[16]=="HUMPHREY VISUAL FIELD" or curr[16]=="GOLDMAN VISUAL FIELD" or curr[16]=="HUMPHREY VISUAL FIELD" or curr[16]=="BIOMETRY" or curr[16]=="PHOTO" or curr[16]=="NEW PATIENT ERG"):
		final_contents[i].insert(17, "dx")
		final_contents[i].insert(18, "blank")
		final_contents[i].insert(19, "blank")
	elif(curr[16]=="NEW PATIENT SAME DAY VISIT" or curr[16]=="NEW PATIENT VISIT RETINA" or curr[16]=="MYHEALTH VIDEO VISIT NPV" or curr[16]=="NEW PATIENT NEURO-OPTHALMOLOGY" or curr[16]=="NEW PATIENT VISIT CORNEA" or curr[16]=="NEW PATIENT VISIT GLAUCOMA" or curr[16]=="NEW PATIENT VISIT INFLAMMATORY" or curr[16]=="NEW PATIENT VISIT OCULOPLASTIC" or curr[16]=="NEW TUMOR VISIT" or curr[16]=="NEW PATIENT PREMATURE" or curr[16]=="NEW PATIENT VISIT CATARACT" or curr[16]=="NEW BINOCULAR VISION EVAL" or curr[16]=="NEW PATIENT VISIT STRABISMUS" or curr[16]=="NPV OPTOMETRIST" or curr[16]=="NEW DYSTROPHY" or curr[16]=="NEW PATIENT VISIT REFRACTION" or curr[16]=="NEW PATIENT VISIT OPTOMETRIST" or curr[16]=="NEW PATIENT COMPREHENSIVE" or curr[16]=="NEW VISION SERVICE PLAN" or curr[16]=="OPHT URGENT" or curr[16]=="NEW PATIENT VISIT RETINA 10" or curr[16]=="NEW PATIENT CORNEA"):
		final_contents[i].insert(17, "new")
		final_contents[i].insert(18, "new")
		if(curr[16]=="MYHEALTH VIDEO VISIT NPV"):
			final_contents[i].insert(19, "tele")
		else:
			final_contents[i].insert(19, "office")
	elif(curr[16]=="POST OP" or curr[16]=="POST-OPERATIVE WEEK ONE VISIT" or curr[16]=="POST-OPERATIVE DAY ONE VISIT" or curr[16]=="PRE OP 15" or curr[16]=="OPHT POSTOP" or curr[16]=="POST OP CORNEA"):
		final_contents[i].insert(17, "peri_op")
		final_contents[i].insert(18, "blank")
		final_contents[i].insert(19, "blank")
	elif(curr[16]=="RETURN PATIENT VISIT 15" or curr[16]=="MYHEALTH VIDEO VISIT RPV" or curr[16]=="RETURN PATIENT VISIT 30" or curr[16]=="RETURN PATIENT VISIT 10" or curr[16]=="SAME DAY RETURN" or curr[16]=="RETURN PATIENT PREMATURE" or curr[16]=="OPHT EST SHORT" or curr[16]=="RETURN PATIENT CORNEA" or curr[16]=="RETURN REFRACTIVE EXAM 15" or curr[16]=="RETURN TUMOR VISIT" or curr[16]=="RETURN BINOCULAR VISION EVAL"):
		final_contents[i].insert(17, "return")
		final_contents[i].insert(18, "return")
		if(curr[16]=="MYHEALTH VIDEO VISIT RPV"):
			final_contents[i].insert(19, "tele")
		else:
			final_contents[i].insert(19, "office")
	elif(curr[16]=="INJECTIONS" or curr[16]=="INJECTION 5" or curr[16]=="CONTACT LENS APPT" or curr[16]=="VISION THERAPY VISIT" or curr[16]=="LASER YAG" or curr[16]=="MINOR PROCEDURE" or curr[16]=="KXL TREATMENT"):
		final_contents[i].insert(17, "rx")
		final_contents[i].insert(18, "blank")
		final_contents[i].insert(19, "blank")
	elif(curr[16]=="STUDY"):
		final_contents[i].insert(17, "study")
		final_contents[i].insert(18, "blank")
		final_contents[i].insert(19, "blank")
	elif(curr[16]=="blank"):
		final_contents[i].insert(17, "blank")
		final_contents[i].insert(18, "blank")
		final_contents[i].insert(19, "blank")
	else:
		final_contents[i].insert(17, "NOTFOUND")
		final_contents[i].insert(18, "NOTFOUND")
		final_contents[i].insert(19, "NOTFOUND")

	#Performing Provider
	editedProvider = curr[30].replace('"', '')
	if(editedProvider=="MONTAGUE, ARTIS ANN - OPHTHALMOLOGY"):
		final_contents[i].insert(31, "cataract")
	elif(curr[30]=="KISTLER, HENRY BLACKMER - OPHTHALMOLOGY" or curr[30]=="LEE, DONNA JAEWHO - OPHTHALMOLOGY"): 
		final_contents[i].insert(31, "comprehensive")
	elif(curr[30]=="LIN, CHARLES CHIA-HONG - OPHTHALMOLOGY" or curr[30]=="TA, CHRISTOPHER NGUYEN - OPHTHALMOLOGY" or curr[30]=="YU, CHARLES QIAN - OPHTHALMOLOGY" or curr[30]=="MANCHE, EDWARD EMANUEL - OPHTHALMOLOGY"): 
		final_contents[i].insert(31, "cornea")
	elif(curr[30]=="BIOMETRY, TECHNICIAN - OPHTHALMOLOGY" or curr[30]=="EYE, PRE-OP - OPHTHALMOLOGY" or curr[30]=="VISUAL FIELD, TECHNICIAN - OPHTHALMOLOGY" or curr[30]=="VISUAL FIELD, TWO - OPHTHALMOLOGY"): 
		final_contents[i].insert(31, "dx")
	elif(curr[30]=="CHANG, ROBERT T - OPHTHALMOLOGY" or curr[30]=="LEE, WEN-SHIN - OPHTHALMOLOGY" or curr[30]=="SINGH, KULDEV - OPHTHALMOLOGY" or curr[30]=="FISHER, ANN CAROLINE - OPHTHALMOLOGY" or curr[30]=="GOLDBERG, JEFFREY LOUIS - OPHTHALMOLOGY" or curr[30]=="SUN, YANG - OPHTHALMOLOGY" or curr[30]=="SHUE, ANN - OPHTHALMOLOGY" or curr[30]=="WANG, SOPHIA YING - OPHTHALMOLOGY"): 
		final_contents[i].insert(31, "glaucoma")
	elif(curr[30]=="LIAO, YAPING JOYCE - OPHTHALMOLOGY" or curr[30]=="MOSS, HEATHER ELSPETH - OPHTHALMOLOGY" or curr[30]=="BERES, SHANNON JEANINE - OPHTHALMOLOGY"): 
		final_contents[i].insert(31, "neuro")
	elif(curr[30]=="BANSAL, SURBHI - OPHTHALMOLOGY" or curr[30]=="BEYER, JILL ELIZABETH - OPHTHALMOLOGY" or curr[30]=="WARNER, KATHERINE ANNE - OPHTHALMOLOGY" or curr[30]=="BINDER, STEVEN WILLIAM - OPHTHALMOLOGY"): 
		final_contents[i].insert(31, "optometry")
	elif(curr[30]=="KOSSLER, ANDREA LORA - OPHTHALMOLOGY" or curr[30]=="ERICKSON, BENJAMIN PETER - OPHTHALMOLOGY" or curr[30]=="WU, ALBERT YA-PO - OPHTHALMOLOGY"): 
		final_contents[i].insert(31, "plastics")
	elif(curr[30]=="SILVA, AMILA RUWAN - OPHTHALMOLOGY" or curr[30]=="LENG, THEODORE - OPHTHALMOLOGY" or curr[30]=="MOSHFEGHI, DARIUS MOHAMMAD - OPHTHALMOLOGY" or curr[30]=="SANISLO, STEVEN RICHARD - OPHTHALMOLOGY" or curr[30]=="MRUTHYUNJAYA, PRITHVI - OPHTHALMOLOGY" or curr[30]=="DO, DIANA V - OPHTHALMOLOGY" or curr[30]=="MAHAJAN, VINIT BHARATI - OPHTHALMOLOGY" or curr[30]=="LEUNG, LOH-SHAN BRYAN - OPHTHALMOLOGY" or curr[30]=="WOOD, EDWARD HUNT - OPHTHALMOLOGY"): 
		final_contents[i].insert(31, "retina")
	elif(curr[30]=="LASER, TECHNICIAN - OPHTHALMOLOGY"): 
		final_contents[i].insert(31, "rx")
	elif(curr[30]=="LAMBERT, SCOTT REED - OPHTHALMOLOGY" or curr[30]=="KOO, EUNA BAUGHN - OPHTHALMOLOGY"): 
		final_contents[i].insert(31, "strabismus")
	elif(curr[30]=="HINKLE, JOHN WILLIAM - OPHTHALMOLOGY" or curr[30]=="VALERIO, GABRIEL SANTOS - OPHTHALMOLOGY" or curr[30]=="NGUYEN, HUY VU - OPHTHALMOLOGY" or curr[30]=="CALLAWAY, NATALIA FIJALKOWSKI - OPHTHALMOLOGY" or curr[30]=="CHARLSON, EMILY SARAH - OPHTHALMOLOGY" or curr[30]=="JHAJ, GURDEEP SINGH - OPHTHALMOLOGY" or curr[30]=="JHAJ, GURDEEP SINGH - OPHTHALMOLOGY" or curr[30]=="CHANG, DOLLY SHUO-TEH - OPHTHALMOLOGY" or curr[30]=="NGUYEN, ANGELINE MICHELLE - OPHTHALMOLOGY" or curr[30]=="RAYESS, NADIM MALEK - OPHTHALMOLOGY"): 
		final_contents[i].insert(31, "urgent")
	elif(curr[30]=="NGUYEN, QUAN DONG - OPHTHALMOLOGY"): 
		final_contents[i].insert(31, "uveitis")
	elif(curr[30]=="blank"):
		final_contents[i].insert(31, "blank")
	else: 
		final_contents[i].insert(31, "NOTFOUND")

	#Race
	if(curr[34]=="Other" or curr[34]=="Asian" or curr[34]=="Black" or curr[34]=="Pacific Islander" or curr[34]=="Native American"):
		final_contents[i].insert(35, "other")
	elif(curr[34]=="White"):
		final_contents[i].insert(35, "white")
	elif(curr[34]=="blank" or curr[34]=="Unknown"):
		final_contents[i].insert(35, "blank")
	else:
		final_contents[i].insert(35, "NOTFOUND")

	#Language
	if(curr[42]=="Mandarin" or curr[42]=="Russian" or curr[42]=="Farsi" or curr[42]=="Vietnamese" or curr[42]=="Cantonese" or curr[42]=="Other" or curr[42]=="Dari" or curr[42]=="Korean" or curr[42]=="Tagalog" or curr[42]=="American Sign Language" or curr[42]=="Hindi" or curr[42]=="Punjabi (Panjabi)" or curr[42]=="Arabic" or curr[42]=="Tongan" or curr[42]=="Amharic" or curr[42]=="Romanian" or curr[42]=="Deaf/Non-Sign Language" or curr[42]=="Japanese" or curr[42]=="Samoan" or curr[42]=="Gujarati" or curr[42]=="Indonesian" or curr[42]=="Albanian" or curr[42]=="Croatian" or curr[42]=="Portuguese" or curr[42]=="Taiwanese"):
		final_contents[i].insert(43, "other")
	elif(curr[42]=="Spanish"):
		final_contents[i].insert(43, "spanish")
	elif(curr[42]=="English"):
		final_contents[i].insert(43, "english")
	elif(curr[42]=="blank" or curr[42]=="Unknown"):
		final_contents[i].insert(43, "blank")
	else:
		final_contents[i].insert(43, "NOTFOUND")

	#Insurance
	if(curr[46]=="MANAGED CARE" or curr[46]=="Blue Cross" or curr[46]=="Blue Shield" or curr[46]=="Managed Care"):
		final_contents[i].insert(47, "commercial")
	elif(curr[46]=="MEDI-CAL MANAGED CARE" or curr[46]=="MEDI-CAL" or curr[46]=="Medi-Cal/CCS" or curr[46]=="Medicaid"):
		final_contents[i].insert(47, "medicaid")
	elif(curr[46]=="Medicare" or curr[46]=="MEDICARE MANAGED CARE"):
		final_contents[i].insert(47, "medicare")
	elif(curr[46]=="Other"):
		final_contents[i].insert(47, "other")
	elif(curr[46]=="blank"):
		final_contents[i].insert(47, "blank")
	else:
		final_contents[i].insert(47, "NOTFOUND")

#Add counter2
final_contents[0].append("counter2")
checker2_dict = {}
for i in range(1,len(final_contents)):
	curr = final_contents[i]
	currID = curr[58]
	if(curr[18] == "new" or curr[18] == "return"):
		if currID not in checker2_dict:
			checker2_dict[currID] = 1
			final_contents[i].append(1)
		else:
			checker2_dict[currID] = checker2_dict[currID] + 1
			final_contents[i].append(checker2_dict[currID])
	else:
		final_contents[i].append("blank")
	
#Write to output file
final_output_file = open(output_name, "w")
final_fileTotal = ""
for i in range(len(final_contents)):
	curr = final_contents[i]
	for j in range(len(curr)):
		final_fileTotal += str(curr[j])
		if(j!=len(curr)): final_fileTotal += "\t"
	if(i!=len(final_contents)): final_fileTotal += "\n"
final_output_file.writelines(final_fileTotal)
final_output_file.close()
print "File " + output_name + " was created."
		










