Run simulator for only one sample:
>> make
>> java Main arg1 arg2 arg3 arg4 arg5

** arg1: which algorithm to use (0:Bottleneck, 1:iASK, 2:SOS)
** arg2: arrival rate of questions raised by each user following a Poisson process 
(0 -> each user asks 1 question every 10 hours
1 -> each user asks 1 question every 6 hours
2 -> each user asks 1 question every 4 hours
3 -> each user asks 1 question every 2 hours
1 -> each user asks 1 question every 1 hour)
** arg3: the seed for generate questions randomly (can be any integer)
** arg4: predictability(a real from 0 to 1)
** arg5: the number of expertise per question

Run simulator for 5 of times:
>> make
>> sh run_3_algo.sh

** please feel free to edit the run_3_algo.h for the # of run you want.

To delete all the *.class
>> make clean

output files are in results/users, results/questions, and results/log, respectively:

1) [AlgorithmType]_[arg2]_[arg3]_[arg4]_user_info,txt:
[user id, total # of passing, total # of answering, average # of passing, average # of answering, # of friends the user passes to]

2) [AlgorithmType]_[arg2]_[arg3]_[arg4]_question_info.txt:
[question id, asker id, # of being passed, # of being answered, [a list of time that every answerer spent], # of invalid answerers]

3) [AlgorithmType]_[arg2]_[arg3]_[arg4]_log.txt:
[question id, passer or answerer, user id, timestamp(second)]
