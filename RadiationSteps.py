## Script for parsing Role01 (Radiation) output files, writing timesteps where LW/SW Radiation
## are called to a CSV. Prints to console the number of times Radiation was called, and the
## average and standard deviation of the times, NOT INCLUDING THE FIRST CALL
## Based on time parsing script written by Dylan Dickerson (UWYO)
## Modified by Suzanne Piver and Henry O'Meara (UWYO), and Cena Miller (NCAR) 

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

def stdev(avg, arr):
    vari = 0;
    for num in arr:
        vari += ((num - avg) ** 2)
    sdev = (vari/len(arr)) ** 0.5
    return sdev
   
# Open and the output file
f = open(args.fileName[0],"r")
text = f.read()

# Extract the lines we care about. matches is a list of strings like:
#   Timing for integration step: 1.05685 s
matches = re.findall("RUNNING LW RADIATION SCHEME\n  Timing for integration step: .*s", text)

# Get a list of the times (calling map returns a map)
times = list(map(extractTime, matches))
timesNoInit = list()
f = open('radiationsteps.csv', 'a')
i = 0
while(i < len(times)):
    f.write('%d;Timing for Integration Step;%f\n' %(i, times[i]))
    if (i>0):
        timesNoInit.append(times[i])
    i = i+1

average = mean(timesNoInit)
SDev = stdev(average, timesNoInit)

print("\nRadiation Calls: " + str(len(times)))
print("Average Integration Time (Not Including Initial): " + str(average))
print("Standard Deviation (Not Including Initial): " + str(SDev))
