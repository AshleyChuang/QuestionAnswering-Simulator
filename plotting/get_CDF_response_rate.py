import sys
import os

rate_b = []
rate_iask = []
rate_sos = []
path = '../results/questions/'

fin1 = open('../results/questions/Bottleneck/Bottleneck_%s_%s_%s_%s_question_info.txt' % (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
fin2 = open('../results/questions/iASK/iASK_%s_%s_%s_%s_question_info.txt' % (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
fin3 = open('../results/questions/SOS/SOS_%s_%s_%s_%s_question_info.txt' % (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
	
for line in fin1:
	lineArr = line.strip().split(",")
	lineArr[4] = lineArr[4].replace("[", "")
	lineArr[4] = lineArr[4].replace("]", "")
	response = lineArr[4].split(" ")
	valid = float(len(response))
	invalid = float(lineArr[5])
	rate_b.append(valid/(valid+invalid)*100)
	
for line in fin2:
	lineArr = line.strip().split(",")
	lineArr[4] = lineArr[4].replace("[", "")
	lineArr[4] = lineArr[4].replace("]", "")
	response = lineArr[4].split(" ")
	valid = float(len(response))
	invalid = float(lineArr[5])
	rate_iask.append(valid/(valid+invalid)*100)

for line in fin3:
	lineArr = line.strip().split(",")
	lineArr[4] = lineArr[4].replace("[", "")
	lineArr[4] = lineArr[4].replace("]", "")
	response = lineArr[4].split(" ")
	valid = float(len(response))
	invalid = float(lineArr[5])
	rate_sos.append(valid/(valid+invalid)*100)
print "bottle = " + str(rate_b) + ";"
print "iask = " + str(rate_iask) + ";"
print "sos = " + str(rate_sos) + ";"
