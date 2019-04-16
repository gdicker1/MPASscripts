# Script to automate benchmarking project for MPAS
#  Currently only configured to run on Cheyenne

import os
import string
import argparse
from subprocess import call

# Global lists
replaceTokens = ['@NNODES', '@NCPUS', '@MPIPROCS', '@HOURS', '@OUTFILE']
resFolders = ['120k', '60k', '30k', '15k', '10k'] # Used to create paths for weak/strong scalings

# TODO: Add functions to parse outputs

def replaceAndMakeNewFile(inFile, nodes, ncpus, res, hours, path, outFile=''):
    ''' Find the replace tokens in inFile and replace them with arguments to this function
        Returns the name of the new file
    '''
    
    w_hours = '{:02d}'.format(hours) # make sure we don't overwrite hours
    if outFile == '':
        outFile = '{0:d}node_{1:d}ncpus_{2:s}res'.format(nodes, ncpus, res)
    newFile = os.path.join(path, outFile + '_job.sh')

    with open(inFile, 'r') as fileIn:
        with open(newFile, 'w') as fileOut:
           for line in fileIn:
                theLine = line.replace(replaceTokens[0],
                                       nodes)
                theLine = theLine.replace(replaceTokens[1],
                                          ncpus)
                theLine = theLine.replace(replaceTokens[2],
                                          ncpus)
                theLine = theLine.replace(replaceTokens[3],
                                          w_hours)
                theLine = theLine.replace(replaceTokens[4],
                                          outFile)
                fileOut.write(theLine)

    return newFile

def launchJob(fName, path):
    ''' Use subprocess.call and qsub to launch a job
    '''
    currDir = os.getcwd()
    os.chdir(path) # Go into benchmark folder for given resolution
    call(['chmod', '755', fName])  # Ensure the script is executable
    call(['qsub' , fName]) # Launch job
    os.chdir(currDir) # Go back to main benchmark folder

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n','--nnodes', help = 'number of compute nodes to run on', type=int,
                        default=36)
    parser.add_argument('-c', '--ncpus', help = 'number of cpus per node', type=int,
                        default=0)
    parser.add_argument('-r','--resolution', help = 'resolution folder to run job in', type=str,
                        default='30')
    parser.add_argument('-w','--walltime', help = 'number of hours to run job for', type=int,
                        default=4)
    parser.add_argument('-o','--outfile', help ='output file, file to be run', type=str,
                        default = '')
    parser.add_argument('-i','--infile', help='file to modify, needs to have replace tokens', type=str,
                        default='job.template')
    parser.add_argument('-m', '--mode', help='whether to do a single run, weak scaling, or strong scaling', type=str,
                        default = 'single')
    # TODO: (optional...?) add a archeticture argument to state if on Cheyenne, Casper, PSG, Witherspoon, Comet affects cores per node
    
    argDict = vars(parser.parse_args())
    nodes = argDict['nnodes']
    ncpus = argDict['ncpus']
    res = argDict['resolution']
    hours = argDict['walltime']
    outFile = argDict['outfile']
    iFile = argDict['infile']
    mode = argDict['mode']
    # Validate and/or update command line args
    if ncpus == 0: # Update ncpus
        ncpus = 36 * nnodes # Assumes we are running on Cheyenne
    if 'k' not in res: # Ensure resolution has k with it if not given
        res += 'k'
    path = os.path.join(os.getcwd(), '{:s}_benchmark'.format(res))
    if not os.path.exists(path):
        print("resolution benchmarking directory doesn't exist")
        raise SystemExit
    if mode not in ('single', 'weak', 'strong'):
        print("error in defining mode choose one of 'single', 'weak', or 'strong'")
        raise SystemExit

    if mode == 'single':
        fName = replaceAndMakeNewFile(iFile, nodes, res, hours, path, outFile)
        launchJob(fName, path)

    elif mode == 'weak':
        # Weak scaling increase number of nodes and increase resolution
        #  TODO: Implement the loop for weak scaling
        pass

    elif mode == 'strong':
        # Strong scaling keep resolution constant increase number of nodes
        #  TODO: Implement the loop for strong scaling
        pass        
