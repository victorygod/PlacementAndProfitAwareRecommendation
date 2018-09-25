import numpy as np
from collections import Counter

def getA(transactions,items,maxLength,num):
    #maxLength --- the largest length of input sets
    #number of input sets
    np.random.seed(5)
    
    count = [[i+1,0] for i in range( len(items) ) ]
    
    
    for row in transactions:
        for item in row:
            count[item-1][1]+=1
    count = sorted(count,key = lambda x:x[1],reverse = True)
    source = count[0:100] #Store 100 item with highest support
    
    A = []    
    for i in range(num):
        length = 0
        while length == 0:
            length = np.random.randint(maxLength)
        index = np.unique([np.random.randint(100) for i in range(length)])
        index = index.tolist()
        tmp = []
        
        for j in index:
            t = source[int(j)][0]
            tmp.append(t)
        if i == 1: print(index)
        tmp.sort()
        A.append(set(tmp))
#    #A.sort()
#    #A = set(A)
    return A

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
    weights = np.array([((counter[x]/n)**gamma)*profits[x-1] for x in counter])
    res = np.array([[x, counter[x]/n, profits[x-1], ((counter[x]/n)**gamma)*profits[x-1]] for x in counter])
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
    transactions = getTransactions("./Experiment/retail.txt")
    items = getItems(transactions)
    #np.random.seed(10)
    profits = np.random.random(size=(len(items))).tolist()
    clickRate = [0.1,0.1,0.1,0.1,
                0.05,0.05,0.05,0.05,
                0.01,0.01,0.01,0.01]
    #A = {1291, 1456, 2476}
    #A = {24, 186, 339, 372, 406, 476, 741, 773, 1147}
#    A={49}
    A = getA(transactions,items,5,100)
    #print(A)
    gamma = 0.5
    while gamma<3.1:
        eop, eoc = 0, 0
        for a in A:
            res = getTopK(transactions, a, profits, gamma = gamma)
            p, c = getProfitExpectation(res, clickRate)
            eop+=p
            eoc+=c
        print("%.1f"%gamma,'\t', eop,'\t', eoc)
        gamma+=0.1
    