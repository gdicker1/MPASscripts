import re
import argparse

parser = argparse.ArgumentParser(description="Evaluate integration times from an output file")
parser.add_argument('fileName', nargs=1, help="Filename of the output file. Example: log.atmosphere.0000.out")
# For debugging
# args = parser.parse_args(['.\log.atmosphere.0000.out'])
args = parser.parse_args()

# Function to extract the time from the lines formatted like:
#   Timing for integration step: 1.05685 s
def extractTime(line):
    result = re.findall("\d+\.\d+", line)
    return float(result[0])

def mean(arr):
    sum = 0;
    for num in arr:
        sum += num
    return sum / len(arr)

# Open and the output file
f = open(args.fileName[0],"r")
text = f.read()

# Extract the lines we care about. matches is a list of strings like:
#   Timing for integration step: 1.05685 s
matches = re.findall("Timing for integration step: .*s", text)

# Get a list of the times (calling map returns a map)
times = list(map(extractTime, matches))

print("Integration Times:")
print(times)

average = mean(times)
print("\nAverage Integration Time: " + str(average))
