# bigraph class
# last edit: 10/15
################CHANGES############
# _buildEmission()
# _updateEmission()
##########TODO##############
# 
######################BUGS#######################
#
##############CURRENTLY WORKING ON##########
#

from operator import itemgetter
import string



class Bigraph:

	def __init__(self):
		self._joint1 = {}														# list of bigram joint probs for beginning of word: [(char1,char2),prob]
		self._conditional1 = {}													# dict of bigram conditional probs for beginnning of word
		self._prior = {}														# start of program

		self._joint2 = {}														# list of bigram joint probs for other positions in word
		self._conditional2 = {}													# dict of bigram conditional probs for other positions in word

		self._emissionProbs = {}												# emission prob dict: [char,prob]

		self._topList = []														# list of top 3 most next most probable letters
		self._f1name = 'bgramFreq1.txt'											# bigram frequencies to be read in
		self._f2name = 'bgramFreq2.txt'
		self._f3name = 'bgramFreq3.txt'
		
		self._start()



	def _start(self):
		"""
		This funtion reads in bigram frequencies from a text file, and calls functions which
		build the joint and conditonal probability tables
		"""
		val = 1																	#flatten out distribution
		
		freqs1 = self._readFile(self._f1name)
		freqs2 = self._readFile(self._f2name)
		freqs3 = self._readFile(self._f3name)

		freqs1 = self._addN(freqs1,val)  										#get rid of all zeros
		freqs2 = self._addN(freqs2,val)
		freqs3 = self._addN(freqs3,val)

		alphabet = map(chr,range(97,123))										######### HACK #############
		for lett in alphabet:													#add [SPC] and [DEL] to both tables of frequency
			sCount = float(2)
			dCount = float(30)
			freqs1.append(((lett,'[SPC]'),sCount))
			freqs1.append(((lett,'[DEL]'),dCount))
			freqs2.append(((lett,'[SPC]'),sCount))
			freqs2.append(((lett,'[DEL]'),dCount))

		self._joint1 = self._buildGraph(freqs1)									#self._joint1{'a':{'a':prob,'b':prob,etc..}}		
		self._prior = self._getPrior()											#calculate prior probabilities

		self._conditional1 = self._joint1
		self._conditional1['[SPC]'] = self._prior
		for key in self._conditional1:
			self._conditional1[key] = self._normalize(self._conditional1[key])	#prob of alphabet given any letter = 1

		self._joint2 = self._buildGraph(freqs2)									#self._joint2{'a':{'a':prob,'b':prob,etc..}}		

		for key in self._joint2:												#build 2nd table of conditionals
			self._conditional2[key] = self._normalize(self._joint2[key])
		


################################## fxns for hidden markov model #######################

	def _getPrior(self):
		"""
		This function calculates the probability of each letter or word being the first
		Rtns: dict {symbol:probability}
		"""
		prior = {}
		for key in self._joint1:
			prior[key] = sum(self._joint1[key][k] for k in self._joint1[key])	#sum raw counts for each symbol
		return self._normalize(prior)											#make counts for all symbols sum to one



	def _conditionalOn(self,joint):
		"""
		This function calculates the probability of a symbol given the previous symbol, 
		using the table	of joint probabilities
		Args: dict of joint probabilities
		Rtns: dict of conditional probabilities
		"""
		temp = []
		tot = sum(joint[key] for key in joint)									#sum up all joint probabilities
		return self._mult(joint, tot)											#multiply every value by that total



################################### hmm helper functions ############

	def _mult(self, d, mplier):
		"""
		This function multiplies every value in a dictionary by a multiplier
		Args: dictionary, multiplier
		Rtn: products of each value and the multiplier
		"""
		for key in d:
			d[key] = d[key] * mplier
		return d



	def _normalize(self,d):
		"""
		This function normalizes all values in a dict so that they sum to one
		Args: dict{'symbol':val}
		Rtns: normalized dict
		"""
		tot = sum(d[key] for key in d)											#sum of all values in dict
		mplier = float(1) / float(tot)
		return self._mult(d, mplier)											#divide each value by sum



	def _addN(self,d,n):
		"""
		This function adds an amount 'n' to each value in the dictionary argument
		Args: dict, amount to be added to each value
		Rtns: dict{symbol:value+n}
		"""
		return [(item[0], item[1] + n) for item in d]



#################################### graph fxns #####################

	def _buildGraph(self,lst):
		"""
		This function builds a graph of conditional probabilities from the list of joint probabilities
		Args: list of joint probabilities
		Rtns: dictionary of conditional probabilities
		"""
		grph = {}
		for item in lst:
			self._add(grph,item[0][0],item[0][1],item[1])
		return grph



	def _readFile(self, flName):
		"""
		This function reads in bigram frequency values from a text file into a list.
		Text file is formatted: a,a,count,b,count,c,count
							    b,a,count,etc...
		Args: text file name
		Rtns: list of bigrams and associated frequency counts
		"""
		fd = open(flName, 'r')
		lst = []
		for line in fd:
			bits = string.split(line, ',')										#tokenize string
			del(bits[-1])														#delete junk at end
			for i in range(1,len(bits),2):
			    item = [(bits[0], bits[i]), float(bits[i+1]) ]
			    lst.append(item)
		return lst



	def _add(self,bgrph,lett1,lett2,weight):
		"""
		This function builds a dictionary of dictionaries, using bigrams and their associated counts to a graph
		Args: dictionary, first letter of bigram, 2nd letter of bigram, associated count
		"""
		if lett1 not in bgrph:		
			bgrph[lett1] = {lett2:weight}
		elif lett2 not in bgrph[lett1]:
			tmp = bgrph[lett1]
			tmp[lett2] = weight
			bgrph[lett1] = tmp



	def _print(self,grph):
		"""
		This function prints out the graph of bigrams
		Args: dictionary of bigrams and their frequencies
		"""
		for key in grph:
			print key, " : ", grph[key]
			print "-" * 10