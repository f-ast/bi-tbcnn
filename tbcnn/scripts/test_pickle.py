import pickle

with open("./data/algorithm_trees.pkl","r") as f:
	data = pickle.load(f)

testing_set = data[1]
training_set = data[0]
labels = data[2]

print "A sample tree : " + str(training_set[0])

print "total number of trees : " + str(len(testing_set) + len(training_set))
print "training trees : " + str(len(training_set))
print "testing trees : " + str(len(testing_set))
print "classes : " + str(labels) 