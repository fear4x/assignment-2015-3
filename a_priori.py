import sys
import csv
import argparse
from collections import defaultdict

def returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet):
		_itemSet = set()
        localSet = defaultdict(int)

        for item in itemSet:
                for transaction in transactionList:
                        if item.issubset(transaction):
                                freqSet[item] += 1
                                localSet[item] += 1

        for item, count in localSet.items():
                support = count
                if support >= int(minSupport):
                        _itemSet.add(item)
        return _itemSet

def joinSet(itemSet, length):
	return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])

def getItemSetTransactionList(data_iterator):
    transactionList = list()
    itemSet = set()
    for record in data_iterator:
        transaction = frozenset(record)
        transactionList.append(transaction)
        for item in transaction:
            itemSet.add(frozenset([item]))
    return itemSet, transactionList

def runApriori(data_iter, minSupport):
    itemSet, transactionList = getItemSetTransactionList(data_iter)
    freqSet = defaultdict(int)
    largeSet = dict()
    oneCSet = returnItemsWithMinSupport(itemSet,transactionList, minSupport,freqSet)
    currentLSet = oneCSet
    i = 2
    while(currentLSet != set([])):
        largeSet[i-1] = currentLSet
        currentLSet = joinSet(currentLSet, i)
        currentCSet = returnItemsWithMinSupport(currentLSet,transactionList, minSupport, freqSet)
        currentLSet = currentCSet
        i += 1

    def getSupport(item):
            return freqSet[item]
    toRetItems = []
    for key, value in largeSet.items():
        toRetItems.extend([(tuple(item), getSupport(item)) for item in value])
    return toRetItems

def fileReader(fname):
        file_iter = open(fname, 'r')
        csv_reader = csv.reader(file_iter, delimiter=',')
        for line in csv_reader:
            line = [field.strip().lower() for field in line]
            record = frozenset(line)
            yield record

def fileReader2(fname):
        file_iter = open(fname, 'r')
        csv_reader = csv.reader(file_iter, delimiter=',')
        for line in csv_reader:
            line = [int(field) for field in line]
            record = frozenset(line)
            yield record

def printDict(itemdct):
        sortedItems = sorted(itemdct.items(), key=lambda x: len(x[0]))
        keyLen = 1
        row = []
        for itm in sortedItems:
            if keyLen != len(itm[0]):
                keyLen = len(itm[0])
                print( ';'.join('%s:%s' % entry for entry in row))
                row = []
            row.append(itm)
        if row != []:
            print( ';'.join('%s:%s' % entry for entry in row))

if __name__ == "__main__":
    parser = argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--numeric", help="items are numeric",
                        action="store_true", default=False)
    parser.add_argument("support", help="support threshold")
    parser.add_argument("-p", "--percentage",
                        action="store_true", default=False,
                        help="treat support threshold as percentage value")
    parser.add_argument("filename", help="input filename")
    parser.add_argument("-o", "--output", type=str, help="output file")

    args = parser.parse_args()

    inFile = fileReader(args.filename)
    minSupport = args.support
    outFile = args.output
    items = runApriori(inFile, minSupport)
    itemdct = dict(items)

    if inFile == None :
        print('No input specified')
        sys.exit()
    if args.numeric:
        inFile = fileReader2(args.filename)
    if args.output:
        sys.stdout = open(outFile, 'w')
        printDict(itemdct)
    else:
        printDict(itemdct)
