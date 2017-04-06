import numpy
fin = open('1_2_hop_adjacencylist.csv');

num_of_links = 0
total_link_delay = 0
link_delay = []

for line in fin:
	lineArr = line.strip().split(",")
	num_of_links += len(lineArr)-1
	for i in range(1, len(lineArr)):
		node = lineArr[i].split(":")
		link_delay.append(int(node[1]))

delay_arr = numpy.array(link_delay)
print "average of link delay: " + str(numpy.mean(delay_arr, axis = 0))
print "std of link delay: " + str(numpy.std(delay_arr, axis = 0))
print "num_of_links: " + str(num_of_links/2.0)
