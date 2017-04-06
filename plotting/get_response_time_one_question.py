import sys
fin1 = open("../results/questions/Bottleneck/Bottleneck_%s_%s_%s_%s_question_info.txt" % (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
fin2 = open("../results/questions/iASK/iASK_%s_%s_%s_%s_question_info.txt" % (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
fin3 = open("../results/questions/SOS/SOS_%s_%s_%s_%s_question_info.txt" % (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))

question_id = sys.argv[5]
lis1 = []
lis2 = []
lis3 = []

for line in fin1:
	lineArr = line.strip().split(',')
	lineArr[4] = lineArr[4].replace("[", "");
	lineArr[4] = lineArr[4].replace("]", "");
	if question_id != lineArr[0]:
		continue
	if lineArr[4] == "": 
		continue
	response_time = lineArr[4].split(" ");
	for t in response_time:
		hour = float(t)/3600.0
		lis1.append(hour)
for line in fin2:
	lineArr = line.strip().split(',')
	lineArr[4] = lineArr[4].replace("[", "");
	lineArr[4] = lineArr[4].replace("]", "");
	if question_id != lineArr[0]:
		continue
	if lineArr[4] == "":
		continue
	response_time = lineArr[4].split(" ");
	for t in response_time:
		hour = float(t)/3600.0
		lis2.append(hour)
for line in fin3:
	lineArr = line.strip().split(',')
	lineArr[4] = lineArr[4].replace("[", "");
	lineArr[4] = lineArr[4].replace("]", "");
	if question_id != lineArr[0]:
		continue
	if lineArr[4] == "":
		continue
	response_time = lineArr[4].split(" ");
	for t in response_time:
		hour = float(t)/3600.0
		lis3.append(hour)
final_lis = []
av_lis1 = reduce(lambda x, y: x + y, lis1) / len(lis1)
av_lis2 = reduce(lambda x, y: x + y, lis2) / len(lis2)
av_lis3 = reduce(lambda x, y: x + y, lis3) / len(lis3)
lis1 = sorted(lis1)
lis2 = sorted(lis2)
lis3 = sorted(lis3)
print "["
for i in range(0, len(lis1)):
	print str(lis1[i])+" "+str(lis2[i])+" "+str(lis3[i]) + ";"
	final_lis.append(lis1[i])
	final_lis.append(lis2[i])
	final_lis.append(lis3[i])
#print str(av_lis1)+" "+str(av_lis2)+";"
print "];"
