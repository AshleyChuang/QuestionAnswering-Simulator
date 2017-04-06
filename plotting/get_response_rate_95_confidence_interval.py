import math
import sys
import scipy as sp
import scipy.stats
import numpy as np
import os

path1 = "../results/questions/Bottleneck/"
path2 = "../results/questions/iASK/"
path3 = "../results/questions/SOS/"

bottle = []
for filename in os.listdir(path1):
	if filename.endswith('.txt'):
		fin = open('../results/questions/Bottleneck/%s' % (filename))
		bottle_rate = []
		for line in fin:
			lineArr = line.strip().split(",")
			lineArr[4] = lineArr[4].replace("[", "")
			lineArr[4] = lineArr[4].replace("]", "")
			response = lineArr[4].split(" ")
			valid = float(len(response))
			invalid = float(lineArr[5])
			bottle_rate.append((valid/(valid+invalid))*100.0)
		bottle.append(bottle_rate)

iask = []
for filename in os.listdir(path2):
	if filename.endswith('.txt'):
		fin = open('../results/questions/iASK/%s' % (filename))
		iask_rate = []
		for line in fin:
			lineArr = line.strip().split(",")
			lineArr[4] = lineArr[4].replace("[", "")
			lineArr[4] = lineArr[4].replace("]", "")
			response = lineArr[4].split(" ")
			valid = float(len(response))
			invalid = float(lineArr[5])
			print "valid: " + str(valid)
			print "invalid: " + str(invalid)
			iask_rate.append((valid/(valid+invalid))*100)
		iask.append(iask_rate)
sos = []
for filename in os.listdir(path3):
	if filename.endswith('.txt'):
		fin = open('../results/questions/SOS/%s' % (filename))
		sos_rate = []
		for line in fin:
			lineArr = line.strip().split(",")
			lineArr[4] = lineArr[4].replace("[", "")
			lineArr[4] = lineArr[4].replace("]", "")
			response = lineArr[4].split(" ")
			valid = float(len(response))
			invalid = float(lineArr[5])
			print "valid: " + str(valid)
			print "invalid: " + str(invalid)
			iask_rate.append((valid/(valid+invalid))*100)
		sos.append(sos_rate)
bottle_mean = []
bottle_std = []
for i in bottle:
	bottle_mean.append(reduce(lambda x, y: x + y, i) / len(i))
	bottle_std.append(np.std(i))
iask_mean = []
iask_std = []
for i in iask:
	iask_mean.append(np.mean(i))
	iask_std.append(np.std(i))

sos_mean = []
sos_std = []
for i in sos:
	sos_mean.append(np.mean(i))
	sos_std.append(np.std(i))
bottle_error = []
iask_error = []
sos_error = []
for i in range(0, len(bottle_std)):
	bottle_error.append((1.96 * bottle_std[i]) / math.sqrt(len(bottle_std)))
	iask_error.append((1.96 * iask_std[i])/ math.sqrt(len(iask_std)))
	sos_error.append((1.96 * sos_std[i]) / math.sqrt(len(sos_std)))
bottle_mean_avg = reduce(lambda x, y: x + y, bottle_mean) / len(bottle_mean)
iask_mean_avg = reduce(lambda x, y: x + y, iask_mean) / len(iask_mean)
sos_mean_avg = reduce(lambda x, y: x + y, sos_mean) / len(sos_mean)
bottle_error_avg = reduce(lambda x, y: x + y, bottle_error) / len(bottle_error)
iask_error_avg = reduce(lambda x, y: x + y, iask_error) / len(iask_error)
sos_error_avg = reduce(lambda x, y: x + y, sos_error) / len(sos_error)
print "["
for i in range(0, len(bottle_mean)):
	print str(bottle_mean[i]) + " " + str(iask_mean[i]) + " " + str(sos_mean[i]) + ";"
print str(bottle_mean_avg) + " " + str(iask_mean_avg) + " " + str(sos_mean_avg) + ";"
print "];"
print "["
for i in range(0, len(bottle_std)):
	print str(bottle_error[i]) + " " + str(iask_error[i]) + " " + str(sos_error[i]) + ";"
print str(bottle_error_avg) + " " + str(iask_error_avg) + str(sos_error_avg) +  ";"
print "];"
	

