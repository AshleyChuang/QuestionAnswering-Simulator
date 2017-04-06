import os
import sys
path = 'results/questions/%s/'%(sys.argv[1])

num_of_questions = 0
total_response_time = 0.0
for filename in os.listdir(path):
	if filename.endswith(".txt"):
		num_of_questions += 1
		fin = open('results/questions/%s/%s' % (sys.argv[1], filename))
		for line in fin:
			lineArr = line.strip().split(",")
			num_of_answerers = int(lineArr[3])
			lineArr[4] = lineArr[4].replace("[", "")
			lineArr[4] = lineArr[4].replace("]", "")
			response_time = lineArr[4].split(" ")
			total = 0.0
			for r in response_time:
				#print "r: " + r
				total += float(r)
			#print total/len(response_time)
		total_response_time += total/len(response_time)
#print num_of_questions
#print total_response_time
print num_of_questions/total_response_time
