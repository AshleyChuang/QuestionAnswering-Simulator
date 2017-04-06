import sys
import os

max_b = []
max_iask = []
max_sos = []
path = '../results/questions/'

fin1 = open('../results/questions/Bottleneck/Bottleneck_%s_%s_%s_%s_question_info.txt' % (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
fin2 = open('../results/questions/iASK/iASK_%s_%s_%s_%s_question_info.txt' % (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))	
fin3 = open('../results/questions/SOS/SOS_%s_%s_%s_%s_question_info.txt' % (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
for line in fin1:
	lineArr = line.strip().split(",")
	lineArr[4] = lineArr[4].replace("[", "")
	lineArr[4] = lineArr[4].replace("]", "")
	if(lineArr[4] == ""):
		continue
	response_time = lineArr[4].split(" ")
	response_time.sort(key=float)
	max_b.append(float(response_time[-1])/3600.0)
	
for line in fin2:
	lineArr = line.strip().split(",")
	lineArr[4] = lineArr[4].replace("[", "")
	lineArr[4] = lineArr[4].replace("]", "")
	if(lineArr[4] == ""):
		continue
	response_time = lineArr[4].split(" ")
	response_time.sort(key=float)
	max_iask.append(float(response_time[-1])/3600.0)

for line in fin3:
	lineArr = line.strip().split(",")
	lineArr[4] = lineArr[4].replace("[", "")
	lineArr[4] = lineArr[4].replace("]", "")
	if(lineArr[4] == ""):
		continue
	response_time = lineArr[4].split(" ")
	response_time.sort(key=float)
	max_sos.append(float(response_time[-1])/3600.0)
print "bottle = " + str(max_b) + ";"
print "iask = " + str(max_iask) + ";"
print "sos = " + str(max_sos) + ";"
