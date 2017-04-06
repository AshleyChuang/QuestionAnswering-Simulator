import re, math, sys, random

import numpy as np

import numpy.linalg as linalg

from collections import Counter

import networkx as nx

import matplotlib.pyplot as plt

from copy import copy

import csv

import re

import json

THRESHOLD=0

fin_posts = open('1_2_hop_post.csv')

fin_active_time = open('1_2_hop_time.csv')

fin_adjacency_list = open('1_2_hop_adjacencylist.csv')

fout_nodes = open('nodes.txt', 'w');

fout_v = open('v.txt', 'w');

time = []

nodes = []

v = []



net = {}

nodes_with_posts = {}



for line in fin_adjacency_list:

    lineArr = line.strip().split(",")

    name = lineArr[0]

    nodes.append(name)

    nodes_with_posts[name] = []

    friends_edge_delay = {}

    for i in range(1, len(lineArr)):

        friend_delay = lineArr[i].strip().split(":")

        friend_name = friend_delay[0]

        edge_delay = friend_delay[1]

        friends_edge_delay[friend_name] = int(edge_delay)

    net[name] = friends_edge_delay

#print net



fin_posts = open('1_2_hop_post.csv')

for line in fin_posts:

    lineArr = line.strip().split(",")

    name = lineArr[0]

    if name not in nodes:

        continue

    user_posts = []

    for i in range(1, len(lineArr)):

        user_posts.append([lineArr[i]])

        #print user_posts

    nodes_with_posts[name] = user_posts



for node in nodes_with_posts:

    v.append(nodes_with_posts[node])



time_range = {}
for line in fin_active_time:

    lineArr = line.strip().split(",")


    if lineArr[0] not in nodes:

        continue

    user_active_time = []

    for i in range(1, len(lineArr)):

        user_active_time.append(int(lineArr[i]))
    
    time.append(user_active_time)

    time_range[lineArr[0]] = []
    for i in range(1, len(lineArr), 2):
        if i>1 and time_range[lineArr[0]][-1][-1] == int(lineArr[i]):
            for ti in range(int(lineArr[i])+1, int(lineArr[i+1])+1):
                time_range[lineArr[0]][-1].append(ti)
        else:
            time_range[lineArr[0]].append(range(int(lineArr[i]), int(lineArr[i+1])+1))
    if time_range[lineArr[0]][-1][-1] == 25 and time_range[lineArr[0]][0][0] == 1:
        time_range[lineArr[0]][-1].extend(time_range[lineArr[0]][0])


#function for finding nearest interval

def nearesttime(time,nodes,check,minNode,s):

##    print minNode

##    print s

    templ=[]

    timestring=' '

    if len(time[nodes.index(minNode)])>2: #if multiple intervals



        for k in range(0,len(time[nodes.index(minNode)]),1):

##            print k

##            print 'hi'

            if k%2==0:

                templ.append(abs(time[nodes.index(s)][0] - time[nodes.index(minNode)][k]))

                timestring=timestring+',('+str(time[nodes.index(minNode)][k])

            else:

                templ.append(1000)

                timestring=timestring+'-'+str(time[nodes.index(minNode)][k])+')'

            minimumdiff=min(j for j in templ if j !=1000)

            pos=templ.index(minimumdiff)

                    #newneighbour is nearest interval

        newneighbor=[time[nodes.index(minNode)][pos],time[nodes.index(minNode)][pos+1]] # nearest time interval calculated



    else:

        newneighbor=[time[nodes.index(minNode)][0],time[nodes.index(minNode)][1]] # if single interval return that one

    #print '_______________________________________'

    return newneighbor


def match_interval(interval, intervals):
    
    for _interval in intervals:
        if len(set(interval) & set(_interval)) > 0 and interval[0] != _interval[-1]:
            return True, _interval

    for _interval in intervals:
        for t in _interval:
            if t > interval[-1]:
                return False, _interval
    
    return False, intervals[0]

def time_diff(intervalA, intervalB):

    min_diff = 24
    timeA = intervalA[-1]
    for timeB in intervalB:
        diff = (timeB - timeA) % 24
        if diff < min_diff:
            min_diff = diff
    
    return min_diff

# modified function for finding shortest path with intervals



def find_shortpath_by_cost(net, time_range, nodes, check, s, t):

    cost = {} # the total cost from start node s to each node
    followed = {} # the previous connected node
    followed_cost = {} # the cost from previous node to current node
    followed_question = {}
    interval = { s:time_range[s] }
    remain_nodes = nodes[:] # to store the nodes haven't been used
    question_time = time_range[s][0]
    followed_question[s] = question_time

    # initialize the cost of each node
    for node in nodes:
        cost[node] = 999999999
    cost[s] = 0
    
    min_node = s # the starting node
    remain_nodes.remove(s)
    removed_nodes = []
    removed_nodes.append(s)
    while (remain_nodes):
        """ 
        find the node (min_node)
        which contains the lowest cost to be achieved during every iteration
        """
        for rnode in removed_nodes:
            question_time = followed_question[rnode]
            for node in net[rnode]:
#        for node in net[min_node]:
                if node not in remain_nodes: continue
            
                penalty = 0.
            
                #matched, _interval = match_interval( interval[min_node], time_range[node] )
                matched, _interval = match_interval( [question_time], time_range[node] )
                if not matched:
                    penalty = time_diff([question_time], _interval)
                    penalty *= 3600
            
#                new_cost = cost[min_node] + net[min_node][node] + penalty
                new_cost = cost[rnode] + net[rnode][node] + penalty

                if new_cost < cost[node]:
                    cost[node] = new_cost
                    #followed[node] = min_node
                    followed[node] = rnode
                    #followed_cost[node] = str(net[min_node][node] + penalty)
                    followed_cost[node] = str(net[rnode][node] + penalty)
                    interval[node] = _interval
                    followed_question[node] = (question_time+penalty/3600) % 24
        
        min_cost = cost[remain_nodes[0]]
        min_node = remain_nodes[0]
        for node in remain_nodes:
            if cost[node] < min_cost:
                min_cost = cost[node]
                min_node = node
        
#        print min_node, interval[min_node]
        if min_cost == 999999999:
            return -1,-1,-1,-1,-1
         
        if min_node == t: break
        remain_nodes.remove(min_node)
        removed_nodes.append(min_node)
    
    path_node = []
    path_cost = []
    path_interval = []
    path_question = []
    node = t
    while(node != s):
        path_node.append("'"+node+"'")
        path_cost.append(followed_cost[node])
        path_interval.append(str(interval[node]))
        path_question.append(str(followed_question[node]))
        node = followed[node]
    path_node.append("'"+s+"'")
    path_cost.append('0.0')
    path_interval.append(str(interval[s]))
    path_question.append(str(time_range[s][0]))

    return path_node[::-1], path_cost[::-1], cost[t], path_interval[::-1], path_question[::-1]


def find_shortpath(net, time_range, nodes, check, s, t):
    """
    net: the adjacent Graph
    time: the available times of each people
    nodes: the list of people
    ** check: not used in this function, you can delete this one **
    s: source
    t: target
    """

    if net.has_key(s)==False:
        return "There is no start node called " + str(s) + "."

    if net.has_key(t)==False:
        return "There is no terminal node called " + str(t) + "."

    cost = {} # the total cost from start node s to each node
    original_cost = {}
    followed = {} # the previous connected node
    followed_cost = {} # the cost from previous node to current node
    followed_original_cost = {} # the cost from previous node to current node
    followed_question = {}
    interval = { s:time_range[s] }
    remain_nodes = nodes[:] # to store the nodes haven't been used
    question_time = time_range[s][0]
    followed_question[s] = question_time

    # initialize the cost of each node
    for node in nodes:
        cost[node] = 9999999999
        original_cost[node] = 9999999999
    cost[s] = 0
    original_cost[s] = 0
    
    min_node = s # the starting node
    remain_nodes.remove(s)
    removed_nodes = []
    removed_nodes.append(s)
    while (remain_nodes):
        """ 
        find the node (min_node)
        which contains the lowest cost to be achieved during every iteration
        """
        for rnode in removed_nodes:
            for node in net[rnode]:
                question_time = followed_question[rnode]
                if node not in remain_nodes: continue
            
                penalty = 0.
            
                #matched, _interval = match_interval( interval[min_node], time_range[node] )
                matched, _interval = match_interval( [question_time], time_range[node] )
                if not matched:
                    penalty = time_diff([question_time], _interval)
                    penalty *= 3600
            
                #new_cost = cost[min_node] + net[min_node][node] + penalty
                new_cost = cost[rnode] + net[rnode][node] + penalty
                #new_original_cost = original_cost[min_node] + net[min_node][node]
                new_original_cost = original_cost[rnode] + net[rnode][node]

                if new_original_cost < original_cost[node]:
                    cost[node] = new_cost
                    original_cost[node] = new_original_cost
                    #followed[node] = min_node
                    followed[node] = rnode
                    #followed_cost[node] = str(net[min_node][node] + penalty)
                    followed_cost[node] = str(net[rnode][node] + penalty)
                    #followed_original_cost[node] = str(net[min_node][node])
                    followed_original_cost[node] = str(net[rnode][node])
                    followed_question[node] = (question_time+penalty/3600) % 24
                    interval[node] = _interval    
            
        min_cost = original_cost[remain_nodes[0]]
        min_node = remain_nodes[0]
        for node in remain_nodes:
            if original_cost[node] < min_cost:
                min_cost = original_cost[node]
                min_node = node
        if min_cost == 9999999999:
            return -1,-1,-1,-1,-1,-1,-1

        if min_node == t: break
        remain_nodes.remove(min_node)
        removed_nodes.append(min_node)

    path_node = []
    path_cost = []
    path_original_cost = []
    path_interval = []
    path_question = []
    node = t
    while(node != s):
        path_node.append("'"+node+"'")
        path_cost.append(followed_cost[node])
        path_original_cost.append(followed_original_cost[node])
        path_interval.append(str(interval[node]))
        path_question.append(str(followed_question[node]))
        node = followed[node]
    path_node.append("'"+s+"'")
    path_cost.append('0.0')
    path_original_cost.append('0.0')
    path_interval.append(str(interval[s]))
    path_question.append(str(time_range[s][0]))
    
    return path_node[::-1], path_original_cost[::-1], path_cost[::-1], original_cost[t], cost[t], path_interval[::-1], path_question[::-1]



#function for finding shortest path with intervals

#function for finding shortest path with intervals
def shortpath_withintervals(net, time,nodes,check,s, t):

    # sanity check
    #if s == t:
        #return "The start and terminal nodes are the same. Minimum distance is 0."
    if net.has_key(s)==False:

        return "There is no start node called " + str(s) + "."
    if net.has_key(t)==False:
        return "There is no terminal node called " + str(t) + "."
    # create a labels dictionary
    labels={}
    newlabel={}
    # record whether a label was updated
    order={}
    # for saving node and edge time
    edge=[]
    nodetime={}
    edgetime={}
    # populate an initial labels dictionary
    for i in net.keys():
        if i == s: labels[i] = 0 # shortest distance form s to s is 0
        else: labels[i] = float("inf") # initial labels are infinity

    from copy import copy
    drop1 = copy(labels) # used for looping
    ## begin algorithm
    firsttime=1
    checkagain=s

    while len(drop1) > 0:
        #print len(drop1)
        # find the key with the lowest label
        minNode = min(drop1, key = drop1.get) #minNode is the node with the smallest value / drop1.get gives us values . in which we then the minimum key
        newneighbor=nearesttime(time,nodes,check,minNode,s)
        caltime=0
        # update labels for nodes that are connected to minNode
        for i in net[minNode]:

            if labels[i] > (labels[minNode] + net[minNode][i]+caltime):
                #finding nearest time interval if multiple intervals
                newneighbor=nearesttime(time,nodes,check,i,minNode)
                #print newneighbor
                    ########################################################
                if time[nodes.index(minNode)][0]<=newneighbor[1] and newneighbor[0]<=time[nodes.index(minNode)][1]: #if overlaping
                    caltime=0
                    nodetime[i]=0
                else: #adding time with weight if not overlaping
                    if newneighbor[0]==time[nodes.index(minNode)][0]:
                        caltime=0
                    else:

                        if newneighbor[0]<time[nodes.index(minNode)][0]:
                            caltime=(24+newneighbor[0]-time[nodes.index(minNode)][1])*3600
                        else:
                            caltime=(abs(newneighbor[0]-time[nodes.index(minNode)][1])*3600)
                #print caltime
                labels[i] = labels[minNode]+net[minNode][i]+caltime
                newlabel[i]= labels[minNode]+net[minNode][i]+caltime
                drop1[i] = labels[minNode] + net[minNode][i]+caltime #add the node to be added
                order[i] = minNode #assign value to du for comparison
                edgetime[i]=labels[i]
                #print labels[i]
                 #find edge for appending
                for key,value in net.iteritems():
                    if key==minNode:
                        for k,val in value.iteritems():
                            if val==net[minNode][i]:
                                edge.append(k)
            #print '-----------------------'
        del drop1[minNode] # once a node has been visited, it's excluded from drop1
        #print drop1
        #print '+++++++++++++++++++++++++++++++++++++++++'
    ## end algorithm
    # print shortest path
    temp = copy(t)
    rpath = []
    path = []
    while 1:
        rpath.append(temp)
        if order.has_key(temp): temp = order[temp]
        else: return "There is no path from " + str(s) + " to " + str(t) + "."
        if temp == s:
            rpath.append(temp)
            break
    for j in range(len(rpath)-1,-1,-1):
        path.append(rpath[j])

    return ("Actual path from " + s + " to " + t + " is " + str(path) + ". Distance on this path with interval is " + str(newlabel[t]) + ".")

#function for finding shortest path without intervals and distance on that path with intervals
def shortest_path_without_interval(net,check, s, t):
    # sanity check
    if s == t:
        return "The start and terminal nodes are the same. Minimum distance is 0."
    if net.has_key(s)==False:
        return "There is no start node called " + str(s) + "."
    if net.has_key(t)==False:
        return "There is no terminal node called " + str(t) + "."
    # create a labels dictionary
    labels={}

    # record whether a label was updated
    order={}
    newvalue={}
    edge=[]
    runfirsttime=1
    # populate an initial labels dictionary
    for i in net.keys():
        if i == s: labels[i] = 0 # shortest distance form s to s is 0
        else: labels[i] = float("inf") # initial labels are infinity
    from copy import copy
    drop1 = copy(labels) # used for looping
    newlabel=copy(labels)
    ## begin algorithm

    while len(drop1) > 0:
        # find the key with the lowest label
        minNode = min(drop1, key = drop1.get) #minNode is the node with the smallest label
        newneighbor=nearesttime(time,nodes,check,minNode,s)
        caltime=0
        # update labels for nodes that are connected to minNode
        for i in net[minNode]:
##            print minNode
##            print i
##            print newneighbor
##            print time[nodes.index(minNode)]
            if labels[i] > (labels[minNode] + net[minNode][i]):
                newneighbor=nearesttime(time,nodes,check,i,minNode)
                #print newneighbor
                a=caltime
                #print(str(newneighbor[0])+' '+str(time[nodes.index(s)][1]))
                if time[nodes.index(minNode)][0]<=newneighbor[1] and newneighbor[0]<=time[nodes.index(minNode)][1]: #if overlaping
                    caltime=0
                else: #adding time with weight if not overlaping
                    if newneighbor[0]==time[nodes.index(minNode)][0]:
                        caltime=0
                    else:

                        if newneighbor[0]<time[nodes.index(minNode)][0]:
                            caltime=(24+newneighbor[0]-time[nodes.index(minNode)][1])*3600
                        else:
                            caltime=(abs(newneighbor[0]-time[nodes.index(minNode)][1])*3600)
                #print caltime
                if newlabel[i] > (newlabel[minNode] + net[minNode][i])+a:
                    newlabel[i]= newlabel[minNode]+net[minNode][i]+caltime
##                if i=='v1' or i=='v2':
##                    print newlabel[i]
##                    print 'hi'
                labels[i] = labels[minNode] + net[minNode][i]
                drop1[i] = labels[minNode] + net[minNode][i]
                order[i] = minNode
                #print (str(labels[minNode]) +' '+str(net[minNode][i])+' '+ str(caltime))
                #print newvalue
                for key,value in net.iteritems():
                        if key==minNode:
                            for k,val in value.iteritems():
                                if val==net[minNode][i]:
                                    edge.append(k)
            #print '_________________________________________'
        del drop1[minNode] # once a node has been visited, it's excluded from drop1
        #print '++++++++++++++++++++++++++++++++++++++++++++++++++'
    ## end algorithm
    # print shortest path
    temp = copy(t)
    rpath = []
    path = []
##    print '_____________________________________________________________________'
    while 1:
        path.append(temp)
        if order.has_key(temp): temp = order[temp]
        else: return "There is no path from " + str(s) + " to " + str(t) + "."
        if temp == s:
            rpath.append(temp)
            break
    for j in range(len(rpath)-1,-1,-1):
        path.append(rpath[j])
    for i in xrange(len(edge)):
        if t==edge[i]:
            return "The shortest path from " + s + " to " + t + " is " + str(path) + ". Minimum distance is " +str(labels[t])+ "\nActual distance on this path with interval is " +str(newlabel[t])

# Given a large random network find the shortest path from '0' to '5'



def Jaccard(str1, str2):
    str1 = set(str1.split())
    str2 = set(str2.split())
    return float(len(str1 & str2)) / len(str1 | str2)
def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator

WORD = re.compile(r'\w+')
def text_to_vector(text):
     words = WORD.findall(text)
     return Counter(words)





def eigenvector_centrality(G, max_iter=100, tol=1.0e-6, nstart=None,
                           weight='weight'):
    """Compute the eigenvector centrality for the graph G.

    Uses the power method to find the eigenvector for the
    largest eigenvalue of the adjacency matrix of G.

    Parameters
    ----------
    G : graph
      A networkx graph

    max_iter : interger, optional
      Maximum number of iterations in power method.

    tol : float, optional
      Error tolerance used to check convergence in power method iteration.

    nstart : dictionary, optional
      Starting value of eigenvector iteration for each node.

    weight : None or string, optional
      If None, all edge weights are considered equal.
      Otherwise holds the name of the edge attribute used as weight.

    Returns
    -------
    nodes : dictionary
       Dictionary of nodes with eigenvector centrality as the value.

    Examples
    --------
    >>> G = nx.path_graph(4)
    >>> centrality = nx.eigenvector_centrality(G)
    >>> print(['%s %0.2f'%(node,centrality[node]) for node in centrality])
    ['0 0.37', '1 0.60', '2 0.60', '3 0.37']

    Notes
    ------
    The eigenvector calculation is done by the power iteration method
    and has no guarantee of convergence.  The iteration will stop
    after max_iter iterations or an error tolerance of
    number_of_nodes(G)*tol has been reached.

    For directed graphs this is "left" eigevector centrality which corresponds
    to the in-edges in the graph.  For out-edges eigenvector centrality
    first reverse the graph with G.reverse().

    See Also
    --------
    eigenvector_centrality_numpy
    pagerank
    hits
    """
    from math import sqrt
    if type(G) == nx.MultiGraph or type(G) == nx.MultiDiGraph:
        raise nx.NetworkXException("Not defined for multigraphs.")

    if len(G) == 0:
        raise nx.NetworkXException("Empty graph.")

    if nstart is None:
        # choose starting vector with entries of 1/len(G)
        x = dict([(n,1.0/len(G)) for n in G])
    else:
        x = nstart
    # normalize starting vector
    s = 1.0/sum(x.values())
    for k in x:
        x[k] *= s
    nnodes = G.number_of_nodes()
    # make up to max_iter iterations
    for i in range(max_iter):
        xlast = x
        x = dict.fromkeys(xlast, 0)
        # do the multiplication y^T = x^T A
        for n in x:
            for nbr in G[n]:
                x[nbr] += xlast[n] * G[n][nbr].get(weight, 1)
        # normalize vector
        try:
            s = 1.0/sqrt(sum(v**2 for v in x.values()))
        # this should never be zero?
        except ZeroDivisionError:
            s = 1.0
        for n in x:
            x[n] *= s
        # check convergence
        err = sum([abs(x[n]-xlast[n]) for n in x])
        if err < nnodes*tol:
            return x

    raise nx.NetworkXError("""eigenvector_centrality():
power iteration failed to converge in %d iterations."%(i+1))""")









##def centrality(net,nodes):
##    list_of_lists = []
##    for person, value in sorted(net.iteritems()):
##        titles = []
##        for node in nodes:
##            try:
##                titles.append(value[node])
##            except KeyError:
##                titles.append(0)
##        list_of_lists.append(titles)
##
##    for i in range(0,len(list_of_lists)):
##        for j in range(0,len(list_of_lists[i])):
##            if list_of_lists[i][j]>0:
##                list_of_lists[i][j] =1
##            else:
##                list_of_lists[i][j] =0
##    print list_of_lists
##
##    eigenValues,eigenVectors = linalg.eig(list_of_lists)
##    maxeigen=max(abs(eigenValues))
##    for i in range(len(list_of_lists)):
##        for j in range(len(list_of_lists[i])):
##            if i==j:
##                list_of_lists[i][j]=list_of_lists[i][j]-maxeigen
##    print list_of_lists
######    #print eigenVectors
##    idx = eigenValues.argsort()[::-1]
##    eigenValues = eigenValues[idx]
##    eigenVectors = eigenVectors[:,idx]
##    centrality=eigenVectors[0]
##    print centrality
##    for i in range(1,len(centrality)):
##        centrality[i]=centrality[i].real
##    #print abs(centrality)


# Given a large random network find the shortest path from '0' to '5'
##check=1
##for a in nodes:
##    Actual=shortpath_withintervals(net,time,nodes, check,s='vs', t=a)
##    short=shortest_path_without_interval(net,check, s='vs', t=a)
##    print('___________________________________________________________________________________________________')
##    print (short)
##    print (Actual)
##check=check+1
##
##print('__________________________________________________________________')
##print('__________________________________________________________________')
#a=input('Enter 1 to start Algorithim.: ')
#find centrality of node
##print '_____________________________________________________________________'
if True:
    G=nx.Graph(net)
    centrality=eigenvector_centrality(G)
    total_score=[]
    final_score=[]

    flag=0
    while flag==0:
        #print 'Select Source Node number from' + ' 0 to '+ str(len(nodes)-1)
        #source=str(raw_input('Enter Source Number: '))
        source = sys.argv[1]
        if int(source)<len(nodes) and int(source)>=0:
            flag=1
        else:
            #print ('No node found.')
            flag=0
##    print '_____________________________________________________________________'
    
    #query=str(raw_input('Enter full query:  '))
    query = sys.argv[3] # question
     #jac=Jaccard(cat.upper(),str(i[0]).upper())
    
    j=0

    #find jackard and cosine

    for i in v:



        #jac=Jaccard(cat.upper(),str(i[0]).upper())



        vector1 = text_to_vector(query.upper())

        vector2 = text_to_vector(str(i[:]).upper())

        cos=get_cosine(vector1, vector2)

##        print cos


        jac=0

        total=jac+cos

        total_score.append(total)

        j=j+1

    for i in range(len(v)):

        #final_score.append(total_score[i]*centrality[nodes[i]])
        score = 0.5*total_score[i] + 0.5*(0.7 + random.randint(0, 6)*0.05)
        final_score.append( score )

##    print final_score

    sort_ans=sorted(enumerate(final_score), key=lambda x: x[1])

    flag=0

    while flag==0:

        #print 'Select answerers from' + ' 1 to '+ str(len(nodes)-1)

        #req_num =input("Specify the number of answerers: ")
        req_num = int(sys.argv[2])
        if int(req_num)<=len(nodes) and int(req_num)>0:

            flag=1

        else:

            #print ('Please enter valid inputs')

            flag=0

##    print '_____________________________________________________________________'

    final_ans=sort_ans[-int(req_num):]

##    print final_ans

    for i in range(len(final_ans)):

        if str(final_ans[i][0])==str(source):

            final_ans.remove(final_ans[i])

            final_ans=(sort_ans[-(int(req_num)+1):-(int(req_num))])+final_ans

##    print final_ans

    check=2
    flag=0
    while flag==0:
        #st_time=int(raw_input('Enter starting time of Source node between 1-24: '))
        #st_end= int(raw_input('Enter ending time of Source node between 1-24: '))
        st_time=int(sys.argv[4])
        #print "starting time:", st_time
        st_end= int(sys.argv[5])
        #print "ending time", st_end
        a=[st_time,st_end]
        THRESHOLD = (st_end - st_time)%24
        THRESHOLD *= 3600
        if st_time<=24 and st_time>0  and st_end<=24 and st_end>0 and st_time!=st_end:
            flag=1
        else:
            print ('Please enter valid inputs.')
            flag=0
##    print '_____________________________________________________________________'
    reserve=time[int(source)]
    if int(st_time) > int(st_end):
        time_range[ nodes[int(source)] ] = range(int(st_time), 25) + range(1, int(st_end)+1)
    else:
        time_range[ nodes[int(source)] ] = range(int(st_time), int(st_end)+1)
    #time[int(source)]=a
    distance=[]

check=1
for ind in final_ans:
       
    short=shortest_path_without_interval(net,check, s=str(nodes[int(source)]), t=str(nodes[ind[0]]))
    #print short

    shortest_path, original_cost_path, cost_path, original_cost, cost, interval_path, question_path = find_shortpath(net, time_range, nodes, check, nodes[int(source)], nodes[ind[0]])
    

##    print ""
##    #print "Ask:", nodes[int(source)] + "," + nodes[ind[0]] + "," + "[" + ','.join(shortest_path) + "]" + "," + str(cost)
##    print "Ask:", nodes[int(source)]
##    print "Answer:", nodes[ind[0]]
##    print ""
    
    if cost >= THRESHOLD or cost == -1:
        continue
##        print "**iASK Path with actual dealy**"
##        print "Path: no available path"
##        print "Link-Wise Delay: -"
##        print "Total path Delay: -"
##        print ""
##        print "**The actual delay with interval differences of iASK**"
##        print "Path: no available path"
##        print "Link-Wise Delay: -"
##        print "Total path Delay: -"
##        print ""
    else:
        print nodes[int(source)] + "," + nodes[ind[0]] + "," + "[" + ','.join(shortest_path) + "]" + "," + str(cost)
##        print "**iASK path with expected delay**"
##        print "Path:", ' => '.join(shortest_path)
##        print "Available Session:", ' => '.join(interval_path)
##        print "Question Status:", ' => '.join(question_path)
##        print "Link-Wise Delay:", ' => '.join(original_cost_path)
##        print "Total expected path Delay:", original_cost
##        print ""
##        print "**iASK Path with actual dealy**"
##        print "Path:", ' => '.join(shortest_path)
##        print "Link-Wise delay:", ' => '.join(cost_path)
##        print "The actual path delay of iASK is:", cost
##        print ""
##    
##    shortest_path, cost_path, cost, interval_path, question_path = find_shortpath_by_cost(net, time_range, nodes, check, nodes[int(source)], nodes[ind[0]])
##   
##    if cost == -1:
##        continue
##    
##        print "**Path of Bottleneck**"
##        print "Path: no available path"
##        print "Link-Wise delay: -"
##        print "Total path Delay: -"
##    else:
##        
##        print nodes[int(source)] + "," + nodes[ind[0]] + "," + "[" + ',' .join(shortest_path) + "]" + "," + str(cost)
##        
##        print "**The Path delay of of Bottleneck **"
##        print "Path:", ' => '.join(shortest_path)
##        print "Available Session:", ' => '.join(interval_path)
##        print "Question Status:", ' => '.join(question_path)
##        print "Link-Wise Delay:", ' => '.join(cost_path)
##        print "Total path delay of of Bottleneck is:", cost
##    print '_____________________________________________________________________'


