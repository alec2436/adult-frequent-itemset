import numpy as np
import pandas as pd
from Node import Node
from Tree import Tree
from IndexFromAttributeFPGrowth import getClassTypeIndex

min_support = 15

def start():

	# use pandas to import the data
	df = pd.read_csv("adult_small_categorical.csv", sep=",", encoding="utf8", header=0)

	# converts pandas object to np.ndarray
	transaction_database = df.values

	frequentItemsets = build_frequent_itemsets(transaction_database, 1)

	header_table, root = take_frequent(transaction_database, frequentItemsets)

	show_frequent(header_table, root)

	# print header_table

	# topNode = header_table[3][2]

	# count_of_original = header_table[3][1]
	# sub_frequent_itemset, conditional_pattern_base = build_conditional_pattern_base(topNode,count_of_original, tree)

	# print sub_frequent_itemset

	# sub_header_table = np.zeros(np.shape(sub_frequent_itemset)[0], dtype=np.object)
	# sub_header_table = np.transpose(np.array([sub_frequent_itemset[:, 0], sub_frequent_itemset[:, 1], sub_header_table]))
	
	# rootB = None
	# rootB = tree.createRoot(rootB)

	# sub_header_table, rootB = build_fptree(conditional_pattern_base, sub_frequent_itemset, sub_header_table, rootB, tree)

	# print header_table[3][0]
	# if tree.check_single_path(rootB):
	# 	frequent_patterns_generated(sub_header_table, header_table[3][0])
	# else:
	# 	print "ok"



	# table_length = np.shape(header_table)[0]

	# # frequent_patterns_list = []

	# for k in xrange(0, 1): #table_length):
	# 	numberOfNodeOccurences = 0
	# 	topNode = header_table[table_length-k-1][1]
	# 	tempNode = topNode

	# 	while topNode != None:
	# 		topNode = topNode.next
	# 		numberOfNodeOccurences += 1

	# 	topNode = tempNode

	# 	for j in xrange(0, numberOfNodeOccurences):
	# 		frequentItemsetsInside, conditional_pattern_base, frequent_items = build_conditional_pattern_base(topNode, tree)

	# 		inner_header_table = build_inner_header_table(frequentItemsetsInside, conditional_pattern_base, frequent_items)

	# 		frequent_patterns_generated(inner_header_table, topNode.name)

def show_frequent(header_table, root, item):
	tree = Tree()
	while not tree.check_single_path(root):

		# eventually do this for all node!
		header_line = header_table[1]

		item = header_line[0]
		count_of_original = header_line[1]
		topNode = header_line[2]
		
		conditional_pattern_base = build_conditional_pattern_base(topNode)

		sub_frequent_itemset = build_frequent_itemsets(conditional_pattern_base, count_of_original)

		sub_header_table = np.zeros(np.shape(sub_frequent_itemset)[0], dtype=np.object)
		sub_header_table = np.transpose(np.array([sub_frequent_itemset[:, 0], sub_frequent_itemset[:, 1], sub_header_table]))

		sub_header_table, rootB = build_fptree(conditional_pattern_base, sub_frequent_itemset, sub_header_table)

		show_frequent(sub_header_table, rootB, item)

	frequent_patterns_generated(header_table, item)




def take_frequent(transaction_database, frequentItemsets):

	# this array will represent the item header table with the custon node links
	header_table = np.zeros(np.shape(frequentItemsets)[0], dtype=np.object)
	header_table = np.transpose(np.array([frequentItemsets[:, 0],frequentItemsets[:, 1],header_table]))

	header_table, root = build_fptree(transaction_database, frequentItemsets, header_table)

	return header_table, root

def find_index(all_items, item):
	for i in xrange(0, np.size(all_items)):
		if item == all_items[i]:
			return i
	return -1

def display_header_table(header_table):
	for i in xrange(0, np.shape(header_table)[0]):
		print ""
		n = header_table[i][1]
		if n != 0:
			name = n.name
			count = 1
			n = n.next
			while(n != None):
				count += 1
				n = n.next
			print str(name) + " " + str(count)

def frequent_patterns_generated(inner_header_table, item):

	table_length = np.shape(inner_header_table)[0]
	
	for j in xrange(0, table_length):
		numberOfNodeOccurences = 0
		secondNode = inner_header_table[table_length-j-1][2]
		tempNode = secondNode
		tree = Tree()
		while secondNode != None:
			secondNode = secondNode.next
			numberOfNodeOccurences += 1

		secondNode = tempNode

		root = tree.get_root(secondNode)

		for i in xrange(0, numberOfNodeOccurences):
			# print secondNode.name
			parents_array = np.array([])
			parents_array = tree.get_parents(secondNode, parents_array)
			if np.size(parents_array) > 0:
				parents_array = np.append(parents_array, item)
				print parents_array

			secondNode = secondNode.next

def build_conditional_pattern_base(topNode):
	# this the conditional_pattern_base acts as a transactional database with which to build and mine the fp-tree
	# the inner_header_table is used for the custom node links
	# Creates Conditional (Sub-)Pattern Bases, transactions
	tree = Tree()

	totalCount = 0
	tempNode = topNode
	while topNode != None:
		if topNode.parent.parent != None:
			totalCount += 1
		topNode = topNode.next
	
	topNode = tempNode

	conditional_pattern_base = np.full((totalCount,9),"null", dtype=np.object)

	for i in xrange(0, totalCount):
		parents_array = np.array([])
		parents_array = tree.get_parents(topNode.parent, parents_array)
		for j in xrange(0, np.size(parents_array)):
			index = getClassTypeIndex(parents_array[j])
			conditional_pattern_base[i][index] = parents_array[j]
		topNode = topNode.next

	return conditional_pattern_base

def build_fptree(transaction_database,frequentItemsets, header_table):
	# builds the fptree and the header_table with custom links
	tree = Tree()
	root = tree.createRoot()

	for trans in xrange(0, np.shape(transaction_database)[0]): # for every transaction
			transaction = transaction_database[trans]
			freqItemsTrans = np.array([], dtype=np.int16)
			for i in xrange(0, np.size(transaction)): # for every class in that transaction
				# finds which variables in this transaction are frequent itemsets
				loc = np.where(frequentItemsets[:, 0] == transaction[i]) # have to only look at frequentItemsets first column

				if np.shape(loc)[1] > 0: # checks if any are frequent itemsets
					freqItemsTrans = np.append(freqItemsTrans, loc[0][0])

			if np.shape(freqItemsTrans)[0] > 0:
				freqItemsIndex = freqItemsTrans # used to insert custom links
				freqItemsTrans = frequentItemsets[freqItemsTrans]
				freqItemsTrans[:, 2] = freqItemsIndex # puts the index of header_table in here
				freqItemsTrans = freqItemsTrans[freqItemsTrans[:, 1].argsort()[::-1]]
				node = tree.add(root, freqItemsTrans[0][0])
				# inserts the custom links
				if header_table[freqItemsTrans[0][2]][2] == 0:
					header_table[freqItemsTrans[0][2]][2] = node
				else:
					if node.count == 1:
						tree.insert_link(header_table[freqItemsTrans[0][2]][2], node)

				for j in xrange(1, np.shape(freqItemsTrans)[0]): # for every frequent item class in that transaction
					node = tree.add(node, freqItemsTrans[j][0])
					# inserts custom links
					if header_table[freqItemsTrans[j][2]][2] == 0:
						header_table[freqItemsTrans[j][2]][2] = node
					else:
						if node.count == 1:
							tree.insert_link(header_table[freqItemsTrans[j][2]][2], node)
	return header_table, root

def get_index_of_null(array):
	index = -1

	final_indexes = np.arange(0, np.size(array))

	for i in xrange(0, np.size(array)):
			if array[i] == "null":
				index = i

	if index > -1:
		one = np.arange(0,index)
		two = np.arange((index+1),np.size(array))

		final_indexes = np.append(one,two)

	return final_indexes

def build_frequent_itemsets(numpy_data, count_of_original): # builds the frequent itemsets using pandas to count

	pandas_data = pd.DataFrame(numpy_data)

	frequentItemsetNames = np.array([])
	frequentItemsetCounts = np.array([], dtype=np.int16)

	# cycles through all the class names
	for i in xrange(0, np.shape(numpy_data)[1]):
		# pandas is used to find the count of every unique variable for every class
		classTypeCount = pandas_data.groupby(i).size()

		# pandas gives an array of all the itemsets that are "frequent", greater than the minium support
		fNames = classTypeCount[classTypeCount*count_of_original > min_support].index.values
		fCounts = classTypeCount[classTypeCount*count_of_original > min_support].values
		final_indexes = get_index_of_null(fNames)
		fNames = fNames[final_indexes]
		fCounts = fCounts[final_indexes]

		frequentItemsetNames = np.append(frequentItemsetNames, fNames)
		frequentItemsetCounts = np.append(frequentItemsetCounts, fCounts)

	# array of all the frequent item sets
	# adds a third column that is used later purely for indexing
	frequentItemsets = np.array([frequentItemsetNames,frequentItemsetCounts, np.zeros(np.size(frequentItemsetNames),dtype=np.int16)])
	frequentItemsets = np.transpose(frequentItemsets)

	# sort by support count in descending order
	frequentItemsets = frequentItemsets[frequentItemsets[:, 1].argsort()[::-1]]

	return frequentItemsets

def get_item_index(item):
	return 4

def main():
	start()

if __name__ == '__main__':
  main()