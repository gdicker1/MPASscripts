#!/bin/bash
# Begin LSF Directives
#BSUB -q excl
#BSUB -W @HOURS:00
#BSUB -nnodes @NNODES  ##number of nodes
#BSUB -alloc_flags gpumps
#BSUB -J mpas
#BSUB -o @OUTFILE.out%J
#BSUB -e @OUTFILE.err%J

echo $LD_LIBRARY_PATH
cd @PARPATH
. setup
module load cuda
nvidia-smi
cd @PATH
ulimit -a

## --nrs = number of nodes(resources), tasks_per_rs = number of MPI ranks/resource(node), cpu_per_rs = 7*tasks_per_rs, gpus_per_rs = number of gpus(# of MPI ranks)/resource(node)

jsrun --smpiargs="-gpu" -D CUDA_VISIBLE_DEVICES --nrs @NNODES --tasks_per_rs @MPIPROCS --cpu_per_rs @CPURS --gpu_per_rs @GPURS --rs_per_host 1 --launch_distribution packed --bind packed:7 ./atmosphere_model