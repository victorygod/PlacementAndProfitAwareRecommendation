import numpy as np
from collections import Counter

def getTransactions(path):
	transactions = []
	with open(path, "r") as f:
		for t in f:
			a = t.split()
			transactions.append({int(ai) for ai in a})
			# transactions.append([int(ai) for ai in a])
	return transactions

def getItems(transactions):
	# items = np.concatenate([t for t in transactions])
	# return np.unique(items).tolist()
	items = set()
	for t in transactions:
		items |= t
	return items

def getTopK(transactions, A, profits, gamma = 2, k = 12):
	subset = filter(lambda x: A <= x, transactions)
	counter = Counter()
	n = 0
	for s in subset:
		n+=1
		for x in s-A:
			counter[x]+=1
	weights = np.array([((counter[x]/n)**gamma)*profits[x] for x in counter])
	res = np.array([[x, counter[x]/n, profits[x], ((counter[x]/n)**gamma)*profits[x]] for x in counter])
	indices = np.argpartition(weights, len(weights) - k)[-k:]
	res = res[indices].tolist()
	return sorted(res, key = lambda x:x[1], reverse = True)

def getProfitExpectation(res, clickRate):
	eop = 0
	eoc = 0
	for i, r in enumerate(res):
		eop+=r[1]*r[2]*clickRate[i]
		eoc+=r[1]*clickRate[i]
	return eop, eoc
	

if __name__ == "__main__":
	transactions = getTransactions("retail.txt")
	items = getItems(transactions)
	np.random.seed(10)
	profits = np.random.random(size=(len(items))).tolist()
	clickRate = [0.1,0.1,0.1,0.1,
				0.05,0.05,0.05,0.05,
				0.01,0.01,0.01,0.01]
	A = {1291, 1456, 2476}
	res = getTopK(transactions, A, profits, gamma = 3)
	eop, eoc = getProfitExpectation(res, clickRate)
	print(eop, eoc)
	
	