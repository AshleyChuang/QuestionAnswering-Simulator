import numpy

fin = open('1_2_hop_time.csv')

active = []

for line in fin:
	lineArr = line.strip().split(",")
	active.append((len(lineArr)-1)/2)

active_arr = numpy.array(active)

print "average: " + str(numpy.mean(active_arr, axis = 0))
print "std: " + str(numpy.std(active_arr, axis = 0))
