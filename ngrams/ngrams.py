import random
import csv
import sys
import math
import cmath
import copy
import collections
from collections import Counter

FREQ = 11
PROB = 22

non_distinct = 0
distinct = 0
j = 1

def unigrams(filename, arg):#unigram generation
	f = open(filename)
	contents = f.read()
	contents = contents.replace('\n',' $ ').lower().split()
	contents.insert(0, "$")

	unigram_freq = Counter(contents)

	unigram_prob = copy.deepcopy(unigram_freq)

	length = len(contents) #length of my non-distinct unigrams
	length_1 = len(unigram_freq) #length of my distinct unigrams
	global non_distinct
	non_distinct = length
	global distinct
	distinct = length_1

	for i in unigram_prob:
		unigram_prob[i] = float(unigram_prob[i])/(length-16642)

	if (arg == PROB):
		return unigram_prob
	elif (arg == FREQ):
		return unigram_freq



def bigrams(filename, arg):#Bigram generation
	f = open(filename)
	contents = f.read()
	contents = contents.replace('\n',' $ ').lower().split()
	contents.insert(0, "$")

	new_list = []
	for i in range(len(contents)-1): 
		cur = i	
		nxt = i+1
		if (contents[nxt] != "$"):
			new_list.append(contents[cur] + " " + contents[nxt])

	bigram_freq = Counter(new_list)
	bigram_prob = copy.deepcopy(bigram_freq)

	length = len(new_list)

	unigram_freq = unigrams(filename, FREQ) #calling frequency list

	for k,v in bigram_prob.items():
		first_word = k.split(' ',1)
		bigram_prob[k] = float(v)/unigram_freq[first_word[0]]

	if (arg == PROB):
		return bigram_prob
	elif (arg == FREQ):
		return bigram_freq




def bigrams_smth(filename):
	unigram_freq = unigrams(filename, FREQ)
	bigram_freq = bigrams(filename, FREQ)

	bigram_smth = copy.deepcopy(bigram_freq)
	
	vocub = len(unigram_freq)
	
	for k,v in bigram_smth.items():
		first_word = k.split(' ',1)
		bigram_smth[k] = (float(v) + 1)/(unigram_freq[first_word[0]] + vocub)

	return bigram_smth




def smooth(word, gram_freq):
	smth = 1
	word = word.split()
	smth = float(1)/(gram_freq[word[0]] + distinct) #distinct words
	return smth



def unigram_strip(uni_list, print_list, uni_gram):
	value = 1
	if len(uni_list) > 0:
		print ('{0}{1}{2}'.format('S = ',print_list, '\n'))
		for i in range(len(uni_list)):
			value = value * uni_gram[uni_list[i]]

		if (value == 0):
			print ('Unsmoothed Unigrams, logprob(S) = undefined')
		else:
			val_log = math.log(value, 2)
			print ('{0}{1}'.format('Unsmoothed Unigrams, logprob(S) = ',round(val_log,4)))



def bigram_strip(bi_list, bi_gram, bi_gram_smth, uni_gram_freq):
	if len(bi_list) > 1:
		new_list = []
		for i in range(len(bi_list)-1):
			cur = i	
			nxt = i+1
			new_list.append(bi_list[cur] + " " + bi_list[nxt])
		
		#Bigram without smoothing
		value = 1
		for i in range(len(new_list)):
			if (bi_gram[new_list[i]] == 0):
				value = 0
				break
			else:
				value = value * bi_gram[new_list[i]]

		if (value == 0):
			print ('Unsmoothed Bigrams, logprob(S) = undefined')
		else:
			val_log = math.log(value, 2)
			print ('{0}{1}'.format('Unsmoothed Bigrams, logprob(S) = ',round(val_log,4)))
		
		#Bigram with smoothing
		value_s = 1
		for i in range(len(new_list)):
			if (bi_gram_smth[new_list[i]] == 0):
				value_s = value_s * smooth(new_list[i], uni_gram_freq)
				continue
			else:
				value_s = value_s * bi_gram_smth[new_list[i]]

		val_log_s = math.log(value_s, 2)
		print ('{0}{1}'.format('Smoothed Bigrams, logprob(S) = ',round(val_log_s,4)))
		print ('\n')



def n_gram(train, test):
	unigram_prob = unigrams(train, PROB)
	unigram_freq = unigrams(train, FREQ)
	bigram_prob = bigrams(train, PROB)
	bigram_smth = bigrams_smth(train)

	f = open(test)
	contents = f.read().replace('\n\n','\n')

	temp_list = []
	temp2_list = []
	with open(test) as f:
		for line in f:
			temp1_list = line.strip()
			temp_list = line.strip().lower().split()
			temp2_list = copy.deepcopy(temp_list)
			unigram_strip(temp_list, temp1_list, unigram_prob)
			temp2_list.insert(0, "$")
			bigram_strip(temp2_list, bigram_prob, bigram_smth, unigram_freq)

	return 0 

def temp_create(new_list, bigram):

	dty = []
	data = []
	tty_freq = {}
	tty_prob = {}
	pick = ". ."
	
	ran = random.uniform(0,1)

	for k,v in bigram.items():
		first_word = k.split(' ',1)
		if (first_word[0] == new_list):
			dty.append(k)
			data.append(v)

	tty_freq = dict(zip(dty,data))
	tty_prob = copy.deepcopy(tty_freq)	
	count = sum(tty_freq.values())

	for k,v in tty_prob.items():
		tty_prob[k] = float(v)/count

	tty_ord = collections.OrderedDict(sorted(tty_prob.items(), key=lambda t: t[1]))

	cum = 0
	for k,v in tty_ord.items():
		cum = cum + v
		tty_ord[k] = cum
		if (ran <= cum):
			pick = k
			break

	return pick


def create_sen(new_list, bigram):
	final = []
	final.append(new_list)
	i = 1
	while (i != 10):
		i = len(final)
		next_word = temp_create(final[i-1].lower(), bigram)
		word_list = next_word
		word = word_list.split(' ',1)
		if (word[1] == '.' or word[1] == '?' or word[1] == '!'):
			final.append(word[1])
			break
		else:
			final.append(word[1])
	
	print('{0}{1}{2}{3}'.format('Sentence ',j,': ',' '.join(final)))


def sen_gen(train, gen):

	global j
	bigram_freq = bigrams(train, FREQ)
	temp_tty = {}
	
	num = 10
	with open(gen) as f:
		for line in f:
			print ('{0}{1}'.format('Seed = ',line))
			temp1_list = line.strip()
			temp_list = line.strip().split()
			j = 0
			for i in range(num): 
				j = i+1
				create_sen(temp_list[0], bigram_freq)
			print('\n')
	return 0


if (sys.argv[2] == '-test'):
	#call n-gram model
	result = n_gram(sys.argv[1], sys.argv[3])
elif (sys.argv[2] == '-gen'):
	#call sentence generator
	result = sen_gen(sys.argv[1], sys.argv[3])
