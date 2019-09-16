# MPASscripts

This repository contains scripts to automate the benchmarking process for strong and weak scaling for the GPU development of the Model for Prediction Across Scales (MPAS) at the University of Wyoming's Electrical and Computer Engineering Department. The main repo for that project is at [MPAS Development Repository](https://github.com/cenamiller/MPAS).

## Contents
* [Benchmarking Automation](#benchmarking-automation)
* [Find Timing Integrations](#find-timing-integrations)
* [Contact Info](#contact)

## Benchmarking Automation
Overall goal of this script is to modify existing execution files to make creating execution files and submitting jobs easier. Given a mode, location, and some optional arguments the script will create a copy of one of the execution scripts (depending on location), replace tokens in the copy with needed values, and submit the job from the relevant folder.

### Usage
This script assumes that whatever folder the jobs are submitted in already has the relevant streamlist and namelist files.

#### Single Mode
Submits a single job and requires usage of the `-n NNODES, -t TASKS_PER_RS, -rp RESPATH, -r RESOLUTION, -w WALLTIME` optional arguments, in addition to the `mode` and `location` to create a execution file within the folder designated by `RESPATH` and launches the job from there.

##### Example Usage
`python automateBenchmarking.py single WSC -n 1 -t 6 -rp benchmarking60k -r 60 -w 4 -i execute_WSC.template`

#### Weak/Strong Mode
Loops through variables defined at the top of `automateBenchmarking.py` to generate and submit execution scripts for weak or strong scaling. Requires that users have multiple folders at the same level as `automateBenchmarking.py` with the required namelist and streamlist files for each resolution. Specifically the script expects the following directories to exist:
* `benchmark120k`
* `benchmark60k`
* `benchmark30k`
* `benchmark15k`
* `benchmark10k`

NOTE: This script works best if `-o OUTFILE` option isn't used, as the script will generate many output files that are named appropriately. The `-i INFILE` option is ignored in both of these modes in favor of a location based `execute_*.template` file.

##### Example Usage
`python automateBenchmarking.py mode WSC`

`python automateBenchmarking.py mode CHEYENNE`

#### Output File Name Auto-generation
When the `-o OUTFILE` option isn't used the name of the execution script and the `.out`/`.err` files are automatically generated based on: the number of nodes requested, the mpi ranks, and the dataset resolution being used.

##### Example
If a single run is requested with the following command:

`python automateBenchmarking.py single WSC -n 1 -t 6 -rp benchmarking60k -r 60 -w 4 -i execute_WSC.template`

then the automatically generated execution script would be placed in the `benchmarking60k` folder would be `1node_6mpi_60res_execute.sh`. The job submission would then write output and errors (respectively) to `1node_6mpi_60res.out` and `1node_6mpi_60res.err`.

#### Command Line Help Output
~~~~
automateBenchmarking.py [-h] [-n NNODES] [-t TASKS_PER_RS]
                               [-rp RESPATH] [-r RESOLUTION] [-w WALLTIME]
                               [-o OUTFILE] [-i INFILE]
                               mode location

positional arguments:
  mode                  whether to do a single run, weak scaling, or strong
                        scaling
  location              which cluster this is running on {WSC, cheyenne,
                        casper}

optional arguments:
  -h, --help            show this help message and exit
  -n NNODES, --nnodes NNODES
                        number of resources (nodes) to run on
  -t TASKS_PER_RS, --tasks_per_rs TASKS_PER_RS
                        number of MPI ranks/resource(node)
  -rp RESPATH, --respath RESPATH
                        path to the resolution folder for a single run
  -r RESOLUTION, --resolution RESOLUTION
                        resolution of the job, used for outfile name creation
                        if not specified
  -w WALLTIME, --walltime WALLTIME
                        number of hours to run job for
  -o OUTFILE, --outfile OUTFILE
                        output file, file to be run
  -i INFILE, --infile INFILE
                        file to modify, needs to have replace tokens
~~~~

## Find Timing Integrations
The `findTimingIntegrations.py` script will accept a file name and extract the integration times and report an average. The script will ignore the first 3 reported integration times when computing the average.

### Usage
To use the script, specify the output file to be parsed, or the path to the output file if it isn't in the same directory. Example usage is shown below.

#### Example Usage
~~~~
python findTimingIntegrations.py log.atmosphere.0000.out
~~~~

#### Example Output
~~~~
Integration Times:
[1.05688, 1.06943, 1.05539, 1.0596, 1.05584, 1.05487, 1.05586]

Average Integration Time: 1.058267142857143
~~~~
#### Command Line Help Output
~~~~
findTimingIntegrations.py [-h] fileName

Evaluate integration times from an output file

positional arguments:
  fileName    Filename of the output file. Example: log.atmosphere.0000.out
~~~~

### Contact
Email gdicker1@uwyo.edu with any questions or recommendations.
