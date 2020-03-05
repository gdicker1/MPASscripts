## Script for parsing Role01 (Radiation) output files, writing timesteps where LW/SW Radiation
## are called to a CSV. Prints to console the number of times Radiation was called, and the
## average and standard deviation of the times, NOT INCLUDING THE FIRST CALL
## 
## Example use: python RadiationSteps.py log.atmosphere.role01.0000.out
## 
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
def extractExecutionTime(line):
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
execTimes = list(map(extractExecutionTime, matches))
execTimesNoInit = list()
f = open('radiationsteps.csv', 'a')
i = 0
while(i < len(execTimes)):
    f.write('%d;Timing for Integration Step;%f\n' %(i, execTimes[i]))
    if (i>0):
        execTimesNoInit.append(execTimes[i])
    i = i+1

average = mean(execTimesNoInit)
SDev = stdev(average, execTimesNoInit)

print("\nRadiation Calls (Not Including Initial): " + str(len(execTimes)-1))
print("Average Integration Time (Not Including Initial): " + str(average))
print("Standard Deviation (Not Including Initial): " + str(SDev))
