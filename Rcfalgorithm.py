import rrcf

def rcfalgorithm(data, shingleinput):
	# Set tree parameters
	num_trees = 40
	shingle_size = shingleinput
	tree_size = 256

#	print("step 1")
	# Create a forest of empty trees
	forest = []
	for _ in range(num_trees):
	    tree = rrcf.RCTree()
	    forest.append(tree)
	
	#print(len(data))	
	
	if len(data) < shingle_size:
		return 0.0
     
	# Use the "shingle" generator to create rolling window
	points = rrcf.shingle(data, size=shingle_size)

	# Create a dict to store anomaly score of each point
	avg_codisp = {}

#	print("step 2")

	last_index=0
	# For each shingle...
	for index, point in enumerate(points):
	    # For each tree in the forest...
		for tree in forest:
		# If tree is above permitted size, drop the oldest point (FIFO)
			if len(tree.leaves) > tree_size:
				tree.forget_point(index - tree_size)
		# Insert the new point into the tree
			tree.insert_point(point, index=index)
		# Compute codisp on the new point and take the average among all trees
			if not index in avg_codisp:
				avg_codisp[index] = 0
			avg_codisp[index] += tree.codisp(index) / num_trees
		last_index = index
	codisplist = [values for key,values in avg_codisp.items()]
	
	return codisplist[last_index]

