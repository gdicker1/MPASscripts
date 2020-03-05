# Script to parse a role00 dynamics output file and create a text file with this format for each timestep: 1;2010-10-23_00:00:00;0.335;FL
## Also prints summary to console
## 
## Example use: python DynamicsSteps.py log.atmosphere.role00.0000.out
## 
## Based on time parsing script written by Dylan Dickerson (UWYO)
## Modified by Suzanne Piver and Henry O'Meara (UWYO), and Cena Miller (NCAR) 

import re
import argparse

parser = argparse.ArgumentParser(description="Evaluate integration times from a dynamics output file")
parser.add_argument('fileName', nargs=1, help="Filename of the output file. Example: log.atmosphere.role00.0000.out")
# For debugging
# args = parser.parse_args(['.\log.atmosphere.0000.out'])
args = parser.parse_args()

# Function to extract the time from the lines formatted like:
#   Timing for integration step: 1.05685 s
def extractExecutionTime(line):
    result = re.findall("\d+\.\d+", line)
    return float(result[0])

def extractSimulationTime(line):
    result = re.findall("\d+\-+\d+\-+\d+\_+\d+\:+\d+\:+\d+", line)
    return str(result[0])

def extractRadiationBool(line):
    result = re.findall("[T,F]",line)
    return str(result[0])

## Statistics functions
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


# Open the output file
f = open(args.fileName[0],"r")
text = f.read()

# Extract the lines we care about. matches is a list of strings like:
#   Timing for integration step: 1.05685 s
executionTimeMatches = re.findall("Timing for integration step: .*s", text)
simulationTimeMatches = re.findall("Begin timestep .*",text)
radiationBoolMatches = re.findall("L_RADLW .*",text)


# Get a list of the times (calling map returns a map)
executionTimes = list(map(extractExecutionTime, executionTimeMatches))
simulationTimes = list(map(extractSimulationTime,simulationTimeMatches))
radiationBools = list(map(extractRadiationBool,radiationBoolMatches))

f = open('dynamicssteps.csv', 'a')
i = 0
skip = 1  #Number of initial time steps to skip
execTimesNoInit = list()
radSimTimes = list() 
dynRadTimes = list()
dynNonRadTimes = list()

while(i < len(simulationTimes)):
    f.write('%d;%s;%f;%s\n' %(i, simulationTimes[i], executionTimes[i], radiationBools[i]))
    if (i>(skip-1)):
        execTimesNoInit.append(executionTimes[i])
        if (radiationBools[i]== 'T'):
            radSimTimes.append(simulationTimes[i])
            dynRadTimes.append(executionTimes[i])
        else:
            dynNonRadTimes.append(executionTimes[i])
    i = i+1

average = mean(execTimesNoInit)
SDev = stdev(average, execTimesNoInit)

dynRadAvg = mean(dynRadTimes)
dynRadSDev = stdev(dynRadAvg,dynRadTimes)

dynNonRadAvg = mean(dynNonRadTimes)
dynNonRadSDev = stdev(dynNonRadAvg,dynNonRadTimes)

date,radInterval = radSimTimes[0].split("_",1)
print("\n---------------------")
print("\nSimulation Summary")
print("\n---------------------")
print("\nRadiation Interval: " + str(radInterval))
print("These statistics DO NOT INCLUDE the first " + str(skip) + " timestep(s)")


print("\nIntegration Steps: " + str(len(execTimesNoInit)))
print("\tAvg Integration Time: " + str(average))
print("\tStd Dev: " + str(SDev))

print("\nIntegration Steps WITH Radiation: " + str(len(radSimTimes)))
print("\tAvg Integration Time: " + str(dynRadAvg))
print("\tStd Dev: " + str(dynRadSDev))

print("\nIntegration Steps WITHOUT Radiation: " + str(len(execTimesNoInit)-len(radSimTimes)))
print("\tAvg Integration Time: " + str(dynNonRadAvg))
print("\tStd Dev: " + str(dynNonRadSDev))



