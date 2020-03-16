import statistics
import random
import csv

# Basic implementation of BST-like structure is inspired by and at points flat out modified from https://www.geeksforgeeks.org/binary-search-tree-set-1-search-and-insertion/

class split():
    def __init__(self, key, subset, comparison, feature, threshold):
        self.right=None
        self.left=None
        self.key=key
        self.data=subset # subset of data stored in node
        self.comparison=comparison # is it checking if data is more or less than threshold
        self.feature=feature # what feature is it using to split
        self.threshold=threshold # what is the threshold

class decision_tree():
    def insert(self, root, node): # standard BST insert taken from geeksforgeeks, compressed, then modified
        if root is None:
            root = node
        else:
            if root.key < node.key:
                if (root.right is None):
                    root.right=node
                else:
                    self.insert(root.right, node)
            else:
                if (root.left is None):
                    root.left=node
                else:
                    self.insert(root.left, node)
    def check_accuracy(self, pile):
        labels=[]
        for i in pile: # FINDS LABELS OF EVERYTHING IN PILE
            labels.append(i[0])
        if len(labels)>2:
            accuracy = statistics.stdev(labels) # FIND ACCURACY OF SORT
        elif len(labels)==1 or len(labels)==0:
            accuracy = 0.0
        elif labels[0]==labels[1]:
            accuracy = 0.0
        else:
            accuracy = 0.5
        return accuracy
    def create_split(self, data, comparison):
        feature = random.randint(1,4) # choose feature for a split
        featurelist = [] # lower data down to just the feature-specific data
        for e in data:
            featurelist.append(e[feature])

        threshold = statistics.mean(featurelist) # initial threshold for split
        prev_total = 2 # initialize previous total variable so improvement calculations work
        improvement = 0
        loops = 0
        direction=1

        while improvement >= 0:
            print ("Improvement this round was %s" % improvement)
            if loops != 0: 
                threshold=prev-10 if direction == -1 else prev+10
            exo, non=[], []
            for e in data: # SORTS DATA BY THRESHOLD
                if comparison == ">":
                    exo.append(e) if e[feature] > threshold else non.append(e)
                if comparison == "<":
                    exo.append(e) if e[feature] < threshold else non.append(e)
            exo_accuracy=self.check_accuracy(exo)
            non_accuracy=self.check_accuracy(non)
            total = exo_accuracy + non_accuracy
            improvement = prev_total-total
            prev_switched=False
            log=[[2, 2]]
            if improvement==0 and prev_improvement==0 and loops > 5 and prev_switched != True:
                print ("Improvement rates are at 0! Switching threshold direction.")
                direction = -direction
                log[0]=[total, threshold]
            prev_switched=True
            if improvement==0 and prev_improvement==0 and loops > 5: # STOP IT FROM GETTING STUCK AT 0 IMPROVEMENT
                if total > log[0][0]:
                    threshold=log[0][1]
                print ("Improvement rates have continued to hit 0 at loop %s! Stopping..." % loops)
                break
            prev = threshold
            prev_total = total
            prev_improvement = improvement
            loops=loops+1
        return [exo, non, comparison, feature, threshold]
    def create_tree(self, depth, current, data, root, loops, key):
        comparisons=['<','>']
        for e in current[0:2]:
            print ("Starting loop %s" % loops)
            print ("big is (%s+%s) and small is (%s-%s)" % (key,2**(depth-loops),key,2**(depth-loops)))
            if e == current[0]:
                key = (key-2**(depth-loops))
                self.insert(root,split(key,current[0], current[2], current[3], current[4]))
            else:
                key = (key+2**(depth-loops))
                self.insert(root,split(key,current[1], current[2], current[3], current[4]))
            if loops >= depth:
                print ('Depth limit exceeded! Stopping...')
                break
            if len(current[0])<1or len(current[1])<1:
                print ('Cannot split list of size <1! Stopping...')
                break
            half = self.create_split(e, comparisons[random.randint(0,1)])
            data.append(half)
            print ("%s <--- this is the key please let it have changed for the love of christ" % key)
            self.create_tree(depth_limit, half, data, root, loops+1, key)
    def inorder(self,root):
        if root:
            self.inorder(root.left)
            print(root.key)
            self.inorder(root.right)



x=decision_tree()
comparisons=['<', '>']
with open('data.csv', 'rt') as f:
    reader = csv.reader(f)
    data = list(reader)
    for a in data:
        for b, c in enumerate(a):
            a[b] = float(a[b])
current = x.create_split(data, comparisons[random.randint(0,1)])
depth_limit=3
root=split(2**depth_limit, data, current[2], current[3], current[4])
x.create_tree(depth_limit, current, [], root, 1, 2**depth_limit)
print("printing treeeee")
x.inorder(root)


