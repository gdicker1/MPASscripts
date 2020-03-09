## Script to parse a role00 dynamics output file and create a text file with
##  this format for each timestep: 1;2010-10-23_00:00:00;0.335;FL
## Also prints summary to console
## 
## Example use: python DynamicsSteps.py -nnodes 72 log.atmosphere.role00.0000.out
## 
## Based on time parsing script written by Dylan Dickerson (UWYO)
## Modified by Suzanne Piver and Henry O'Meara (UWYO), and Cena Miller (NCAR) 

import re
import argparse
import sys
import datetime

parser = argparse.ArgumentParser(description="Evaluate integration times from a dynamics output file")
parser.add_argument('-n', '--nnodes',default=1, help='number of resources (nodes) job ran on', type=int)
parser.add_argument('fileName', nargs=1, help="Filename of the output file. Example: log.atmosphere.role00.0000.out")
# For debugging
# args = parser.parse_args(['.\log.atmosphere.0000.out'])
args = parser.parse_args()

# Parsing regular expressions

def extractJobTime(line):
    result = re.findall("\d+\/+\d+\/+\d+\s+\d+\:+\d+\:+\d+", line)
    return str(result[0])

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
#Returns job time in minutes
def getJobTime(start,end):
    #ed,et = end.split(" ",1)
    #sdate = sd.split("/")
    #stime = st.split(":")
    #edate = ed.split("/")
    #etime = et.split(":")
    stime = datetime.datetime.strptime(start, '%Y/%m/%d %H:%M:%S')
    etime = datetime.datetime.strptime(end, '%Y/%m/%d %H:%M:%S')
    jtime = etime-stime
    return (jtime.total_seconds()/60)
    

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

# Open the output file


f = open(args.fileName[0],"r")
summFile = args.fileName[0].strip(".out")

f_csv = open(summFile+'.00.csv', 'a')
f_csvRad = open(summFile+'.00.JustRad.csv','a')
f_summary = open(summFile+'.00.summary', 'w')
sys.stdout = Tee(sys.stdout, f_summary)
nodes = args.nnodes
text = f.read()

# Extract the lines we care about. matches is a list of strings like:
#   Timing for integration step: 1.05685 s

dynRanks = re.findall("Beginning MPAS-atmosphere Output Log File for task .*", text)
jobStart = re.findall("Opened at .*", text)
jobEnd = re.findall("Closing file at .*", text)
executionTimeMatches = re.findall("Timing for integration step: .*s", text)
simulationTimeMatches = re.findall("Begin timestep .*",text)
radiationBoolMatches = re.findall("L_RADLW .*",text)


# Get a list of the times (calling map returns a map)
jobStart = list(map(extractJobTime, jobStart))
jobEnd = list(map(extractJobTime, jobEnd))
executionTimes = list(map(extractExecutionTime, executionTimeMatches))
simulationTimes = list(map(extractSimulationTime,simulationTimeMatches))
radiationBools = list(map(extractRadiationBool,radiationBoolMatches))

i = 0
skip = 3  #Number of initial time steps to skip
execTimesNoInit = list()
radSimTimes = list() 
dynRadTimes = list()
dynNonRadTimes = list()

f_csv.write('Step;Sim Time Stamp;Integration Time;Radiation Called\n')
while(i < len(simulationTimes)):
    f_csv.write('%d;%s;%f;%s\n' %(i, simulationTimes[i], executionTimes[i], radiationBools[i]))
    if (i>(skip-1)):
        execTimesNoInit.append(executionTimes[i])
        if (radiationBools[i]== 'T'):
            radSimTimes.append(simulationTimes[i])
            f_csvRad.write('%d;%s;%f\n' %(i, simulationTimes[i], executionTimes[i])) 
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
jobTime = round(getJobTime(jobStart[0],jobEnd[0]),2)
print("\n---------------------")
print("Simulation Summary")
print("---------------------")
print("\nNumber of Nodes: " + str(nodes))
print("Total Job Time (mins): " + str(jobTime))
print("Estimated Node Hours: " + str((jobTime*nodes)/60))
print("\nRadiation Interval (HH:MM:SS) : " + str(radInterval))
print("\nThese statistics DO NOT INCLUDE the first " + str(skip) + " timestep(s)")


print("\nIntegration Steps: " + str(len(execTimesNoInit)))
print("\tAvg Integration Time (sec): " + str(average))
print("\tStd Dev: " + str(SDev))

print("\nIntegration Steps WITH Radiation: " + str(len(radSimTimes)))
print("\tAvg Integration Time (sec): " + str(dynRadAvg))
print("\tStd Dev: " + str(dynRadSDev))

print("\nIntegration Steps WITHOUT Radiation: " + str(len(execTimesNoInit)-len(radSimTimes)))
print("\tAvg Integration Time (sec): " + str(dynNonRadAvg))
print("\tStd Dev: " + str(dynNonRadSDev))
print("\n\n")
f.close()
f_summary.close()
with open(args.fileName[0],"r") as infile, open(summFile+'.00.summary', 'a') as outfile:
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

