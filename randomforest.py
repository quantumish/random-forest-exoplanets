import statistics
import random
import csv

# READ FEATURES FROM FILE

with open('output.csv', 'rb') as f:
    reader = csv.reader(f)
    data = list(reader)
    for a in data:
        for b, c in enumerate(a):
            a[b] = float(a[b])

def make_split(prev, data, comparison):
# FIND RANDOM THRESHOLD POINT CODE
    feature = 0
    while feature in prev or feature == 0: # RANDOM FEATURE NOT USED PREVIOUSLY
        feature = random.randint(1,4) 
    findmaxandmin = [] # FIND RANDOM THRESHOLD
    for e in data:
        findmaxandmin.append(e[feature])
#        print e[feature]
#    print findmaxandmin
    mini, maxi = min(findmaxandmin), max(findmaxandmin)
    total=0
    prev_total=2000 # SET UP VARIABLES SO WHILE LOOP DOESNT ERROR OUT
    loops = 0
    threshold = random.randint(round(mini), round(maxi)) # FINALLY DEFINE RANDOM THRESHOLD
    improvement=0
    while improvement >= 0: # BEGIN "TRAINING" WHILE LOOP
        print improvement
        if loops != 0:
            threshold=prev-10 # ARBITRARY, MIGHT INCLUDE ADDITION, BUT DECREASES THRESHOLD BY STEPS
        exo=[]
        non=[]
        for e in data: # SORTS DATA BY THRESHOLD
            if comparison == "more":
                if e[feature] > threshold:
                    exo.append(e)
                else:
                    non.append(e)
            if comparison == "less":
                if e[feature] < threshold:
                    exo.append(e)
                else:
                    non.append(e)
        labels_exo=[] 
        for i in exo: # FINDS LABELS OF EVERYTHING IN EXO PILE
            labels_exo.append(i[0])
        if len(labels_exo)>2: 
            exo_accuracy = statistics.stdev(labels_exo) # FIND ACCURACY OF SORT
        else:
            exo_accuracy = 999
        labels_non=[]
        for i in non: # FINDS LABELS OF EVERYTHING IN NON PILE
            labels_non.append(i[0])
        if len(labels_non)>2:
            non_accuracy = statistics.stdev(labels_non) # FIND ACCURACY OF SORT
        else:
            non_accuracy = 999
        total = exo_accuracy + non_accuracy
        improvement = prev_total-total
        if improvement==0 and prev_improvement==0: # STOP IT FROM GETTING STUCK AT 0 IMPROVEMENT
            break
        prev = threshold
        prev_total = total
        prev_improvement = improvement
        loops=loops+1
    return [exo, non, labels_exo, labels_non, exo_accuracy, non_accuracy, feature]


# BUGGY RECURSION BELOW:

#def make_tree(depth_limit, current, everything, loops):
#    comparisons=['less', 'more']
#    for e in current[0:2]:
#        print "LOOP" + str(loops)
#        if loops >= depth_limit:
#            print 'DEPTH_EXCEEDED'
#            break
#        half = make_split([current[-1]], e, comparisons[random.randint(0,1)])
#        everything.append(half)
#        make_tree(depth_limit, half, everything, loops+1)
#    print 'SHOULD OUTPUT BELOW AND STOP'
#    return everything



comparisons=['less', 'more']
current = make_split([], data, comparisons[random.randint(0,1)])
print 'final accuracies'
print current[4], current[5]
#print "hi"
#print len(make_tree(3, current, [], 1))


