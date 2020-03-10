import statistics
import random
import csv

# READ FEATURES FROM FILE

with open('data.csv', 'rb') as f:
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
    print "Chose feature #%s!" % (feature) 
    featurelist = [] # FIND RANDOM THRESHOLD
    for e in data:
        featurelist.append(e[feature])

    total = 0
    prev_total = 2000 # SET UP VARIABLES SO WHILE LOOP DOESNT ERROR OUT
    loops = 0
    threshold=statistics.mean(featurelist)
    improvement=0

    while improvement >= 0: # BEGIN "TRAINING" WHILE LOOP
        print "Improvement this round was %s" % improvement
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
        if len(labels_exo)<0.2*len(labels_non) and loops > 5:
            print "Split is too unbalanced at loop %s! Stopping..." % loops
            break
        improvement = prev_total-total
        prev_switched=False
        if improvement==0 and prev_improvement==0 and loops < 5 and prev_switched != True:
            print "Improvement rates are at 0! Switching threshold direction."
            if comparison == "more":
                comparison = "less"
            if comparison == "less":
                comparison = "more"
            prev_switched=True
        if improvement==0 and prev_improvement==0 and loops > 5: # STOP IT FROM GETTING STUCK AT 0 IMPROVEMENT
            print "Improvement rates have continued to hit 0 at loop %s! Stopping..." % loops
            break
        prev = threshold
        prev_total = total
        prev_improvement = improvement
        loops=loops+1
    return [exo, non, labels_exo, labels_non, exo_accuracy, non_accuracy, feature]


# BUGGY RECURSION BELOW:

def make_tree(depth_limit, current, everything, loops):
    comparisons=['less', 'more']
    for e in current[0:2]:
        print "Starting loop %s" % loops
        if loops >= depth_limit:
            print 'Depth limit exceeded! Stopping...'
            break
        half = make_split([current[-1]], e, comparisons[random.randint(0,1)])
        everything.append(half)
        make_tree(depth_limit, half, everything, loops+1)
    print 'Done!'
    return everything


comparisons=['less', 'more']
current = make_split([], data, comparisons[random.randint(0,1)])
depth_limit=input("Depth limit? ")
output=make_tree(depth_limit, current, [], 1)[-(2**(depth_limit)):]
print '\nOriginal exoplanet pile has accuracy of %s for %s items, and original non-exoplanet pile has accuracy of %s for %s items.\n' % (current[4], len(current[2]), current[5], len(current[3]))


total=0
for e in output:
    print "Exoplanet accuracy is %s for %s items. Non-exoplanet accuracy is %s for %s items" % (e[4],len(e[2]),e[5],len(e[3]))
    total=total+len(e[2])+len(e[3])

print total, len(data)

