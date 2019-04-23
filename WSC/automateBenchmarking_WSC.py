# Script to automate benchmarking project for MPAS
#  Currently only configured to run on WSC

import os
import string
import argparse
from subprocess import call, Popen, wait
from time import sleep

# Global lists
replaceTokens = ['@HOURS', '@OUTFILE', '@PARPATH', '@PATH',
                 '@NNODES', '@MPIPROCS', '@CPURS', '@GPURS']
# Used to create paths for weak/strong scalings
resFolders = ['120k', '60k', '30k', '15k', '10k']

# TODO: Add functions to parse outputs


def replaceAndMakeNewFile(inFile, nodes, mpiranks, cpurs, gpurs, res, hours, path, outFile=''):
    ''' Find the replace tokens in inFile and replace them with arguments to this function
        Returns the name of the new file
    '''

    w_hours = '{:02d}'.format(hours)  # make sure we don't overwrite hours
    if outFile == '':
        outFile = '{0:d}node_{1:d}mpi_{2:s}res'.format(nodes, mpiranks, res)
    newFile = os.path.join(path, outFile + '_execute.sh')
    parpath = os.path.abspath(os.path.join(path, os.pardir))

    with open(inFile, 'r') as fileIn:
        with open(newFile, 'w') as fileOut:
            for line in fileIn:
                theLine = line.replace(replaceTokens[0],
                                       str(w_hours))
                theLine = theLine.replace(replaceTokens[1],
                                          outFile)
                theLine = theLine.replace(replaceTokens[2],
                                          parpath)
                theLine = theLine.replace(replaceTokens[3],
                                          path)
                theLine = theLine.replace(replaceTokens[4],
                                          str(nodes))
                theLine = theLine.replace(replaceTokens[5],
                                          str(mpiranks))
                theLine = theLine.replace(replaceTokens[6],
                                          str(cpurs))
                theLine = theLine.replace(replaceTokens[7],
                                          str(gpurs))
                fileOut.write(theLine)

    return newFile


def launchJob(fName, path):
    ''' Use subprocess.call and qsub to launch a job
    '''
    currDir = os.getcwd()
    os.chdir(path)  # Go into benchmark folder for given resolution
    call(['chmod', '755', fName])  # Ensure the script is executable
    print "Launching interactive shell"
    proc = Popen(['bsub', '-nnodes', '1', '-Is', '-W', '60', '-q', 'excl_int', '$SHELL', universal_newlines=True])
    proc.wait(30)
    # sleep(20)  # Wait because the interactive shell takes a minute to launch
    print "Interactive shell launched, submitting job"
    print fName
    print os.path.exists(fName)
    call(['cat', fName])
    with open(fName) as myinput
    call(['bsub'], stdin=myinput)  # Launch job
    print "Job submitted"
    call(['exit'])  # Close the interactive shell
    print "Interactive shell closed"
    os.chdir(currDir)  # Go back to main benchmark folder


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', help='whether to do a single run, weak scaling, or strong scaling', type=str,
                        default='single')
    parser.add_argument('-n', '--nnodes', help='number of resources (nodes) to run on', type=int,
                        default=1)
    parser.add_argument('-t', '--tasks_per_rs', help='number of MPI ranks/resource(node)', type=int,
                        default=1)
    parser.add_argument('-r', '--resolution', help='resolution folder to run job in', type=str,
                        default='30')
    parser.add_argument('-w', '--walltime', help='number of hours to run job for', type=int,
                        default=3)
    parser.add_argument('-o', '--outfile', help='output file, file to be run', type=str,
                        default='')
    parser.add_argument('-i', '--infile', help='file to modify, needs to have replace tokens', type=str,
                        default='execute_WSC.template')
    # TODO: (optional...?) add a archeticture argument to state if on Cheyenne, Casper, PSG, Witherspoon, Comet affects cores per node

    argDict = vars(parser.parse_args())
    nodes = argDict['nnodes']
    mpiranks = argDict['tasks_per_rs']
    res = argDict['resolution']
    hours = argDict['walltime']
    outFile = argDict['outfile']
    iFile = argDict['infile']
    mode = argDict['mode']
    cpurs = 7*mpiranks
    gpurs = mpiranks/nodes

    # Validate and/or update command line args
    if 'k' not in res:  # Ensure resolution has k with it if not given
        res += 'k'
    if mode not in ('single', 'weak', 'strong'):
        print("error in defining mode choose one of 'single', 'weak', or 'strong'")
        raise SystemExit

    if mode == 'single':
        path = os.path.join(os.getcwd(), 'benchmark{:s}'.format(res))
        if not os.path.exists(path):
            print("resolution benchmarking directory doesn't exist")
            raise SystemExit
        fName = replaceAndMakeNewFile(
            iFile, nodes, mpiranks, cpurs, gpurs, res, hours, path, outFile)
        launchJob(fName, path)

    elif mode == 'weak':
        # Weak scaling increase number of nodes and increase resolution
        #  TODO: Implement the loop for weak scaling
        pass

    elif mode == 'strong':
        # Strong scaling keep resolution constant increase number of nodes
        #  TODO: Implement the loop for strong scaling
        pass
