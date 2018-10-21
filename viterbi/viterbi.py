import sys
import math
import numpy as np

#Emission probability
def emission_prob(filename, tags):
	emis_list = {}
	with open(filename) as f:
		for line in f:
			temp = line.strip().split()
			if temp[0] not in tags:
				word = temp[0]+temp[1]
				emis_list[word] = temp[2]
	
	return emis_list

#Transition probability
def transition_prob(filename, tags):

	trans_list = {} 
	with open(filename) as f:
		for line in f:
			temp = line.strip().split()
			if temp[0] in tags:
				word = temp[0]+temp[1]
				trans_list[word] = temp[2]
	
	return trans_list

#Finding max_score for viterbi
def max_score(t, w, score, transition, tag_list, words):

	new_list = []
	for i in range(len(tag_list)):
		t1 = tag_list[t]+tag_list[i]

		if t1 not in transition:
			transition[t1] = 0.0001
			
		value = float(transition[t1]) * float(score[i][w-1])
		new_list.append(value)

	return new_list

#Finding sum for forward
def sum_score(t, w, score, transition, tag_list, words):

	new_list = []
	for i in range(len(tag_list)):
		t1 = tag_list[t]+tag_list[i]

		if t1 not in transition:
			transition[t1] = 0.0001

		value = float(transition[t1]) * float(score[i][w-1])
		new_list.append(value)

	return sum(new_list)

#Viterbi for POS-tagging
def pos_tag_viterbi(word_list, emission, transition, tags):

	viterbi_score = np.zeros((len(tags),len(word_list)-1))
	back_ptr = np.zeros((len(tags),len(word_list)-1))

	#Initilisation step
	for i in range(0, len(tags), 1):
		trans = tags[i]+word_list[0]
		ems = word_list[1]+tags[i]
		if ems not in emission:
			emission[ems] = 0.0001
		if trans not in transition:
			transition[trans] = 0.0001

		viterbi_score[i][0] = float(emission[ems]) * float(transition[trans])
		back_ptr[i][0] = 0

	#Iteration step
	for w in range(2, len(word_list), 1):
		for i in range(len(tags)):
			ems = word_list[w]+tags[i]
			if ems not in emission:
				emission[ems] = 0.0001

			max_list = max_score(i, w-1, viterbi_score, transition, tags, word_list)
			max_value = max(max_list)
			
			#Findind the max index
			for t in range(len(tags)):
				if max_value == max_list[t]:
					max_index = t

			viterbi_score[i][w-1] = float(emission[ems]) * float(max_value)
			back_ptr[i][w-1] = max_index

	#printing
	for w in range(1, len(word_list), 1):
		for i in range(len(tags)):
			value = math.log((viterbi_score[i][w-1]),2)
			print ("P(%s=%s) = %.4f" % (word_list[w], tags[i], round(value,4)))

	#Back_ptr printing
	print ('\n')
	print ('FINAL BACKPTR NETWORK') 
	for w in range(1, len(word_list)-1, 1):
		for i in range(len(tags)):
			ptr_value = back_ptr[i][w]
			print ('{0}{1}{2}{3}{4}{5}'.format('Backptr(', word_list[w+1], '=', tags[i], ') = ', tags[int(ptr_value)]))


	#Back_tracking
	seq = np.zeros((len(word_list)-1))
	tmp = []

	#finding max_index in the last column
	for w in range(len(word_list)-1, len(word_list), 1):
		for i in range(len(tags)):
			val = viterbi_score[i][w-1]
			tmp.append(val)
		last_max = max(tmp)

		for i in range(len(tags)):
			if last_max == tmp[i]:
				last_index = i

	print ('\n')
	print ("BEST TAG SEQUENCE HAS LOG PROBABILITY = %.4f" % (round((math.log(last_max,2)),4)))
	w = len(word_list)-1 #length without phi
	seq[w-1] = last_index	

	for i in range(w-1, 1, -1):
		seq[i-1] = back_ptr[int(seq[i])][i]
	
	for i in range(len(seq), 0, -1):
		print ('{0}{1}{2}'.format(word_list[i],' -> ',tags[int(seq[i-1])]))
	print ('\n')
		

#Forward algorithm for POS-tagging
def pos_tag_forward(word_list, emission, transition, tags):

	forward_score = np.zeros((len(tags),len(word_list)-1))

	#Initilisation step
	for i in range(0, len(tags), 1):
		trans = tags[i]+word_list[0]
		ems = word_list[1]+tags[i]
		if ems not in emission:
			emission[ems] = 0.0001
		if trans not in transition:
			transition[trans] = 0.0001

		forward_score[i][0] = float(emission[ems]) * float(transition[trans])

	
	#Iteration step
	for w in range(2, len(word_list), 1):
		for i in range(len(tags)):
			ems = word_list[w]+tags[i]
			if ems not in emission:
				emission[ems] = 0.0001

			forward_score[i][w-1] = float(emission[ems]) * sum_score(i, w-1, forward_score, transition, tags, word_list)

	#printing
	for w in range(1, len(word_list), 1):
		col_sum = 0
		for i in range(len(tags)):
			col_sum += forward_score[i][w-1]

		for i in range(len(tags)):
			value = forward_score[i][w-1]
			value = float(value) / col_sum
			print ("P(%s=%s) = %.4f" % (word_list[w], tags[i], round(value,4)))
	
#Part of speech tag list
tag_list = ['noun','verb','inf','prep']

ems_list = emission_prob(sys.argv[1], tag_list)
trans_list = transition_prob(sys.argv[1], tag_list)

with open(sys.argv[2]) as f:
	for line in f:
		print ('{0}{1}{2}'.format('PROCESSING SENTENCE: ', line.strip(),'\n'))
		print ('FINAL VITERBI NETWORK')
		tmp1_list = line.strip().split()
		tmp1_list.insert(0, "phi") 
		pos_tag_viterbi(tmp1_list, ems_list, trans_list, tag_list)
		print ('FORWARD ALGORITHM RESULTS')
		pos_tag_forward(tmp1_list, ems_list, trans_list, tag_list)
		print ('\n')
