# Script to determine the number of partitions that border each partition
# Example usage: python partitionNeighbors.py x1.40962.graph.info x1.40962.graph.info.part.32 
# Henry O'Meara

import sys

graphFile = open(sys.argv[1],'r')
graphLines = graphFile.readlines()
graphFile.close()

partFile = open(sys.argv[2],'r')
partLines = partFile.readlines()
partFile.close()

# Create list of partitions that each cell belongs to
# For example, partList[0] is the partition of the first cell
partList = map(int,partLines)

# Number of partitions equals maxPart+1
# minPart should always be zero
maxPart = max(partList)
minPart = min(partList)

# Create nxn matrix where n is number of partitions
# Bools of whether or not the column number partion borders the row number partiton
partNeighbors = [[0 for x in range(maxPart+1)] for y in range(maxPart+1)]

# Iterate through each cell
cell = 0
for part in partList:
	# Check the partition number of neighboring cells
	neighborCells = graphLines[cell+1].split()
	neighborCells = map(int,neighborCells)
	for neighborCell in neighborCells:
		neighborPart = partList[int(neighborCell-1)]
		# Set value to 1 if neighbor cell is in a different partition
		if neighborPart != part:
			partNeighbors[part][neighborPart] = 1
	cell += 1

# Sum rows of partNeighbors
borderingParts=[0]*(maxPart+1)
for i in range(maxPart+1):
	borderingParts[i] = sum(partNeighbors[i])
	#print('Partitions bordering partition %d: %d' %(i,borderingParts[i]))
	
print('Max border partitions: %d' %(max(borderingParts)))
print('Min border partitions: %d' %(min(borderingParts)))
