# Script to automate benchmarking project for MPAS
#  Currently only configured to run on WSC

import os
import string
import argparse
from subprocess import call
from time import sleep

# Common lists
replaceTokens = ('@HOURS', '@OUTFILE', '@PARPATH', '@PATH',
                 '@NNODES', '@MPIPROCS', '@CPURS', '@GPURS')
# Used to create paths for weak/strong scalings
resFolders = ['120k', '60k', '30k', '15k', '10k']
''' 40k dataset == 120k res 
    163k dataset == 60k res
    655k dataset == 30k res
    2621k dataset == 15k res
    5898k dataset == 10k res
'''
# Other tuples to help make strong/weak scripts
#  These tuples should be long enough to define the number of runs we need
weakNodes = (1, 1, 4, 16, 1, 2, 8, 1)
weakGPUs = weakMPI = (1, 4, 4, 4, 2, 4, 4, 2)
weakCPUs = (7, 28, 28, 28, 14, 28, 28, 7)
weakRes = ('120k', '60k', '30k', '15k', '60k', '30k', '15k', '60k')

strongNodes = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16)
strongGPUs = strongMPI = (6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6)
strongCPUs = (42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42)
strongRes = ('15k', '15k', '15k', '15k', '15k', '15k', '15k', '15k',
             '15k', '15k', '15k', '15k', '15k', '15k', '15k', '15k')


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


def launchJob(fName, path, location):
    ''' Use subprocess.call and qsub to launch a job
    '''
    jobSub = ''
    if location == 'WSC':
        jobSub = 'bsub'
    elif location == 'cheyenne':
        jobSub = 'qsub'
    elif location == 'casper':
        jobSub = 'sbatch'
    else:
        return
    currDir = os.getcwd()
    os.chdir(path)  # Go into benchmark folder for given resolution
    call(['chmod', '755', fName])  # Ensure the script is executable
    call([jobSub, fName])  # Launch job
    os.chdir(currDir)  # Go back to main benchmark folder


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'mode', help='whether to do a single run, weak scaling, or strong scaling', type=str)
    parser.add_argument(
        'location', help='which cluster this is running on {WSC, cheyenne, casper}', type=str)
    parser.add_argument('-n', '--nnodes', help='number of resources (nodes) to run on', type=int,
                        default=1)
    parser.add_argument('-t', '--tasks_per_rs', help='number of MPI ranks/resource(node)', type=int,
                        default=1)
    parser.add_argument(
        '-rp', '--respath', help='path to the resolution folder for a single run', type=str)
    parser.add_argument('-r', '--resolution', help='resolution of the job, used for outfile name creation if not specified', type=str,
                        default='30')
    parser.add_argument('-w', '--walltime', help='number of hours to run job for', type=int,
                        default=3)
    parser.add_argument('-o', '--outfile', help='output file, file to be run', type=str,
                        default='')
    parser.add_argument('-i', '--infile', help='file to modify, needs to have replace tokens', type=str,
                        default='execute_WSC.template')

    argDict = vars(parser.parse_args())
    nodes = argDict['nnodes']
    mpiranks = argDict['tasks_per_rs']
    resPath = argDict['resPath']
    res = argDict['resolution']
    hours = argDict['walltime']
    outFile = argDict['outfile']
    iFile = argDict['infile']
    mode = argDict['mode']
    location = argDict['location'].lower()
    cpurs = 7*mpiranks
    gpurs = mpiranks/nodes

    # Validate and/or update command line args
    if mode not in ('single', 'weak', 'strong'):
        print("error in defining mode choose one of \'single\', \'weak\', or \'strong\'")
        raise SystemExit
    if location not in ('wsc', 'cheyenne', 'casper'):
        print(
            "error in defining location choose one of \'wsc\', \'cheyenne\', or \'casper\'")
        raise SystemExit
    if 'k' not in res:  # Ensure resolution has k with it if not given
        res += 'k'

    if mode == 'single':
        if not os.path.exists(resPath):
            print("error resolution path {:s} doesn't exist".format(resPath))
            raise SystemExit
        fName = replaceAndMakeNewFile(
            iFile, nodes, mpiranks, cpurs, gpurs, res, hours, resPath, outFile)
        launchJob(fName, resPath, location)

    elif mode == 'weak':
        # Weak scaling increase number of nodes and increase resolution
        if location == 'wsc':
            iFile = 'execute_WSC.template'
        elif location == 'cheyenne':
            iFile = 'execute_CHEYENNE.template'
        elif location == 'casper':
            iFile = 'execute_CASPER.template'
        for i in range(weakNodes):
            resPath = os.path.join(os.getcwd(), 'benchmark'+weakRes[i])
            fName = replaceAndMakeNewFile(
                iFile, weakNodes[i], weakMPI[i], weakCPUs[i], weakGPUs[i], weakRes[i], 4, resPath)
            launchJob(fName, resPath, location)

    elif mode == 'strong':
        # Strong scaling keep resolution constant increase number of nodes
        if location == 'wsc':
            iFile = 'execute_WSC.template'
        elif location == 'cheyenne':
            iFile = 'execute_CHEYENNE.template'
        elif location == 'casper':
            iFile = 'execute_CASPER.template'
        for i in range(strongNodes):
            resPath = os.path.join(os.getcwd(), 'benchmark'+strongRes[i])
            fName = replaceAndMakeNewFile(
                iFile, strongNodes[i], strongMPI[i], strongCPUs[i], strongGPUs[i], strongRes[i], 4, resPath)
            launchJob(fName, resPath, location)
