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
import sys

parser = argparse.ArgumentParser(description="Evaluate integration times from an output file")
parser.add_argument('fileName', nargs=1, help="Filename of the output file. Example: log.atmosphere.0000.out")
# For debugging
# args = parser.parse_args(['.\log.atmosphere.0000.out'])
args = parser.parse_args()

# Function to extract the time from the lines formatted like:
#   Timing for integration step: 1.05685 s
def extractExecutionTime(line):
    #result = re.findall("\d+\.\d+", line)
    result = re.findall("[+-]?\d+(?:\.\d*(?:[eE][+-]?\d+)?)?", line)
    return float(result[0])

def extractRadiationBool(line):
    result = re.findall("[T,F]",line)
    return str(result[0])

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
# Write Summary to console and file simultaneously 
class Tee(object):
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush() # If you want the output to be visible immediately
    def flush(self) :
        for f in self.files:
            f.flush()   
# Open and the output file
f = open(args.fileName[0],"r")
text = f.read()

# Extract the lines we care about. matches is a list of strings like:
#   Timing for integration step: 1.05685 s
#radSyncMatches = re.findall("RUNNING LW RADIATION SCHEME\n  Timing for integration step: .*s", text)
radiationBoolMatches = re.findall("L_RADLW .*",text)
executionTimeMatches = re.findall("Timing for integration step: .*s", text)

# Get a list of the times (calling map returns a map)
radiationBools = list(map(extractRadiationBool,radiationBoolMatches))
executionTimes = list(map(extractExecutionTime, executionTimeMatches))
execTimesNoInit = list()

RadTimes = list()
NonRadTimes = list()

summFile = args.fileName[0].strip(".out")
f_summary = open(summFile + '.01.summary', 'w')
sys.stdout = Tee(sys.stdout, f_summary)

f_csv = open(summFile + '.01.csv', 'w')
f_csvRad = open(summFile+'.01.JustRad.csv','w')
i = 0
skip = 3  #Number of initial time steps to skip
f_csv.write('Step;LW/SW Radiation Called;Integration Time;\n')

while(i < len(executionTimes)):
    f_csv.write('%d;%s;%f\n' %(i, radiationBools[i], executionTimes[i]))
    if (i>(skip-1)):
        execTimesNoInit.append(executionTimes[i])
        if (radiationBools[i]== 'T'):
            f_csvRad.write('%d;%f\n' %(i, executionTimes[i]))
            RadTimes.append(executionTimes[i])
        else:
            NonRadTimes.append(executionTimes[i])
    i = i+1

average = mean(execTimesNoInit)
SDev = stdev(average, execTimesNoInit)

RadAvg = mean(RadTimes)
RadSDev = stdev(RadAvg,RadTimes)

NonRadAvg = mean(NonRadTimes)
NonRadSDev = stdev(NonRadAvg,NonRadTimes)

print("\n---------------------")
print("Simulation Summary")
print("---------------------")

print("\nThese statistics DO NOT INCLUDE the first " + str(skip) + " timestep(s)")

print("\nNumber Time  Steps: " + str(len(execTimesNoInit)))
print("\tAvg Integration Time (sec): " + str(average))
print("\tStd Dev: " + str(SDev))

print("\nSteps WITH Radiation: " + str(len(RadTimes)))
print("\tAvg Time (sec): " + str(RadAvg))
print("\tStd Dev: " + str(RadSDev))

print("\nSteps WITHOUT Radiation: " + str(len(execTimesNoInit)-len(RadTimes)))
print("\tAvg Time (sec): " + str(NonRadAvg))
print("\tStd Dev: " + str(NonRadSDev))
print("\n\n")
f.close()
f_summary.close()
with open(args.fileName[0],"r") as infile, open(summFile+'.01.summary', 'a') as outfile:
    copy = False
    for line in infile:
        if line.strip() == "Timer information:":
            copy = True
        if copy:
            outfile.write(line)
        if line.strip() == "Critical error messages":
            copy = False

f_csv.close()
f_summary.close()
f.close()
