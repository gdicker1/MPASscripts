#!/bin/bash
# Get tarballs
# This is a huge file. Can take ~10 hours
wget http://www2.mmm.ucar.edu/projects/mpas/benchmark/v5.2/MPAS-A_benchmark_10km_L56_v5.2.tar.gz
wget http://www2.mmm.ucar.edu/projects/mpas/benchmark/v5.2/MPAS-A_benchmark_15km_L56_v5.2.tar.gz
wget http://www2.mmm.ucar.edu/projects/mpas/benchmark/v5.2/MPAS-A_benchmark_30km_L56_v5.2.tar.gz
wget http://www2.mmm.ucar.edu/projects/mpas/benchmark/v5.2/MPAS-A_benchmark_60km_L56_v5.2.tar.gz
wget http://www2.mmm.ucar.edu/projects/mpas/benchmark/v5.2/MPAS-A_benchmark_120km_L56_v5.2.tar.gz
# Unpack tarballs
echo "mkdir -p benchmark120k && tar -xvf MPAS-A_benchmark_120km_L56_v5.2.tar.gz -C benchmark120k --strip-components=1"
mkdir -p benchmark120k && tar -xvf MPAS-A_benchmark_120km_L56_v5.2.tar.gz -C benchmark120k --strip-components=1
echo "mkdir -p benchmark60k && tar -xvf MPAS-A_benchmark_60km_L56_v5.2.tar.gz -C benchmark60k --strip-components=1"
mkdir -p benchmark60k && tar -xvf MPAS-A_benchmark_60km_L56_v5.2.tar.gz -C benchmark60k --strip-components=1
echo "mkdir -p benchmark30k && tar -xvf MPAS-A_benchmark_30km_L56_v5.2.tar.gz -C benchmark30k --strip-components=1"
mkdir -p benchmark30k && tar -xvf MPAS-A_benchmark_30km_L56_v5.2.tar.gz -C benchmark30k --strip-components=1
echo "mkdir -p benchmark15k && tar -xvf MPAS-A_benchmark_15km_L56_v5.2.tar.gz -C benchmark15k --strip-components=1"
mkdir -p benchmark15k && tar -xvf MPAS-A_benchmark_15km_L56_v5.2.tar.gz -C benchmark15k --strip-components=1
echo "mkdir -p benchmark10k && tar -xvf MPAS-A_benchmark_10km_L56_v5.2.tar.gz -C benchmark10k --strip-components=1"
mkdir -p benchmark10k && tar -xvf MPAS-A_benchmark_10km_L56_v5.2.tar.gz -C benchmark10k --strip-components=1
