import numpy
from nltk.corpus import stopwords

fin = open('1_2_hop_post.csv')

total_expertises = []
cachedStopWords = stopwords.words("english")

for line in fin:
	lineArr = line.strip().split(",")
	expertise = 0
	for i in range(1, len(lineArr)):
		text = lineArr[i]
		post = ' '.join([word for word in text.split() if word not in cachedStopWords])
		keywords = post.split(" ")
		expertise += len(keywords)
	total_expertises.append(expertise)

expertise_arr = numpy.array(total_expertises)
print "mean: " + str(numpy.mean(expertise_arr, axis = 0))
print "std: " + str(numpy.std(expertise_arr, axis = 0))
