import numpy as np
import pandas as pd
import scipy.misc # used for combinations
from itertools import combinations, chain
from IndexFromAttribute import getClassTypeIndex

min_support = 15

def start():

	# use pandas to import the data
	df = pd.read_csv("adult_small_formatted.csv", sep=",", encoding="utf8", header=0)

	# converts pandas object to np.ndarray
	adult = df.values

	L = [0]
	"""
	this is a list that will contain a list of objects
	each object in this list will be a frequent itemset
	the index of the object will corresond to which frequent itemset it is
	starts with a 0, which is just there for show
	L[1] will be L1
	"""

	L.append(frequentItemset(1))
	build_L1(L[1], df)

	# print L[1].itemSetArray

	k = 2
	while (k > 0):
		L.append(frequentItemset(k))
		L[k].itemSetArray = L[k-1].join_itemset()
		# if (np.size(L[k].itemSetArray) == 0):
		# 	k *= -1
		# 	break;
		L[k].prune_itemset(L[k-1].itemSetArray)
		# if (np.size(L[k].itemSetArray) == 0):
		# 	k *= -1
		# 	break;
		L[k].check_min_support(adult)
		if (np.size(L[k].itemSetArray) == 0):
			k *= -1
			break;
		k = k + 1

	print L[-1*(k+1)].itemSetArray


class frequentItemset:
	def __init__(self, countType):
		self.countType = countType # whether it's an L1 or L2, L3... frequent itemset etc.
		self.itemSetArray = np.array([])

	def add_itemset(self, itemset): # itemset is added if it satifies the minimum support, used to build L1
		self.itemSetArray = np.append(self.itemSetArray, itemset)

	def check_min_support(self,adult): # takes the frequent itemset array and determines which ones have the required support
		indexArray = np.array([], dtype=np.int32) # will be an array of the indexes of where the count is greater than the minimum support
		
		# try to vectorize this step at some point
		for i in xrange(0, np.shape(self.itemSetArray)[0]):
			# condition will be an array that says whether the minimum count is satsfied
			conditionArray = adult[:, getClassTypeIndex(self.itemSetArray[i][0])] == self.itemSetArray[i][0]

			for j in xrange(1, np.shape(self.itemSetArray)[1]): # loops through every condition
				conditionArray = conditionArray & (adult[:, getClassTypeIndex(self.itemSetArray[i][j])] == self.itemSetArray[i][j])
			supportCount = np.shape(adult[np.where(conditionArray)])[0]
				
			if (supportCount > min_support):
				indexArray = np.append(indexArray, i)
		self.itemSetArray = self.itemSetArray[indexArray]

	def get_itemset_length(self):
		return np.size(self.itemSetArray)

	def join_itemset(self): # the join step
		# number of elements in array should be n Choose (countType + 1)

		# the unique elements are needed to build the combinations  
		unique = np.unique(self.itemSetArray)

		# this will be an array that represents the index values used to generate all the combinations
		indexOfCombinations = combination_index(np.size(unique), self.countType+1)

		# numpy's fancy indexing is used to quickly generate all the combinations needed
		return unique[indexOfCombinations]

	def prune_itemset(self, previosItemSetArray): # prunes the array of itemsets that aren't included in previous itemset

		# will the the index of itemsets that do satisfy the apriopi condition
		indexArray = np.array([], dtype=np.int32)

		# cycle through all item sets that were made in the join
		for i in xrange(0, np.shape(self.itemSetArray)[0]):
			if (self.check_all_itemsets(previosItemSetArray, self.itemSetArray[i])):
				indexArray = np.append(indexArray, i) # if it's satisfied add to the array

		self.itemSetArray = self.itemSetArray[indexArray]
		return self.itemSetArray

	def check_all_itemsets(self, previosItemSetArray, itemsets):
		# builds all the combinations of its subsets and checks if they're in the previous itemset

		# index used to generate all the combinations
		indexOfCombinations = combination_index(np.size(itemsets), np.size(itemsets)-1)

		allCombinations = itemsets[indexOfCombinations]
		for i in xrange(0, np.shape(allCombinations)[0]): # loops through all the combinations and checks if they're in the previous set
			if (not self.check_itemset(previosItemSetArray, allCombinations[i])):
				return False

		self.check_itemset(previosItemSetArray, allCombinations[0])

		return True

	def check_itemset(self, previosItemSetArray, itemset): # checks if a given itemset is in the previous frequent itemset
		
		# array that gives whether the corresponding elements are equal
		checkArray = np.equal(previosItemSetArray, itemset)

		# initialize the evaluation array with the first column
		if (np.shape(checkArray)[0] == np.size(checkArray)): # checks that the array is 2d, for L2 only it's 1d
			checkArrayEvaluated = checkArray
		else:
			checkArrayEvaluated = checkArray[:, 0]

		# for every column find the product of the previous column
		# remember True * True = True, but True * False = False
		if (np.shape(checkArray)[0] != np.size(checkArray)):
			for i in xrange(1, np.shape(checkArray)[1]):
				checkArrayEvaluated *= checkArray[:, i]

		# checks if every item in the given itemset is the exact same as any itemset in the previous itemset
		return np.any(checkArrayEvaluated)

def build_L1(L1, df): # uses pandas for counting to build L1
	# list of the categorical classes, will bin the numerical ones later
	classNamesCategory = ["workclass","education","marital-status","occupation","relationship","race","sex","native-country","incomeBracket"]

	# cycles through all the class names
	for i in xrange(0, np.size(classNamesCategory)):
		# pandas is used to find the count of every unique variable for every class
		classTypeCount = df.groupby(classNamesCategory[i]).size()
		# pandas gives an array of all the itemsets that are "frequent", greater than the minium support
		L1.add_itemset(classTypeCount[classTypeCount > min_support].index.values)


def combination_index(n, k): # generates combinations. specifically the index 
    count = scipy.misc.comb(n, k, exact=True)
    index = np.fromiter(chain.from_iterable(combinations(np.arange(n), k)), 
                        np.int32, count=count*k)
    return index.reshape(-1, k)

def main():
	start()

if __name__ == '__main__':
  main()