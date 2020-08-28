#!/bin/bash

#
# Sources for all libraries used in this script can be found at
# http://www2.mmm.ucar.edu/people/duda/files/mpas/sources/
#

module purge
module load pgi/19.7
module load openmpi/3.1.4
module load cmake
module load cuda


# Where to find sources for libraries
export LIBSRC=/glade/work/cmille73/pgi197/sources

# Where to install libraries
export LIBBASE=/glade/work/cmille73/pgi197/pgi197libs

# Compilers
export SERIAL_FC=pgf90
export SERIAL_F77=pgf90
export SERIAL_CC=pgcc
export SERIAL_CXX=pgc++
export MPI_FC=mpif90
export MPI_F77=mpif90
export MPI_CC=mpicc
export MPI_CXX=mpicxx

export OMPI_CC=$SERIAL_CC
export OMPI_CXX=$SERIAL_CXX
export OMPI_FC=$SERIAL_FC
export OMPI_F90=$SERIAL_FC
export OMPI_F77=$SERIAL_FC

export CC=$SERIAL_CC
export CXX=$SERIAL_CXX
export F77=$SERIAL_F77
export FC=$SERIAL_FC
unset F90  # This seems to be set by default on NCAR's Cheyenne and is problematic
unset F90FLAGS

########################################
# MPICH
########################################
#tar xzvf ${LIBSRC}/mpich-3.3.1.tar.gz
#cd mpich-3.3.1
#export CC=$SERIAL_CC
#export CXX=$SERIAL_CXX
#export F77=$SERIAL_F77
#export FC=$SERIAL_FC
#export CFLAGS="-D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
#./configure --prefix=${LIBBASE} --enable-fortran --enable-romio
#make
#make check
#make install
#cd ..

########################################
# zlib
########################################
export CFLAGS='-D_LARGEFILE64_SOURCE=1 -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE=1'
tar xzvf ${LIBSRC}/zlib-1.2.11.tar.gz
cd zlib-1.2.11
./configure --prefix=${LIBBASE} --static
make 
make install
cd ..
#rm -rf zlib-1.2.11
#
#########################################
## HDF5
#########################################
tar xjvf ${LIBSRC}/hdf5-1.10.5.tar.bz2
cd hdf5-1.10.5
unset  CFlags
export FC=$MPI_FC
export CC=$MPI_CC
export CXX=$MPI_CXX
#
./configure --prefix=${LIBBASE} --enable-parallel --with-zlib=${LIBBASE} --disable-shared 
#
make
#make check
make install
cd ..
##rm -rf hdf5-1.10.5

########################################
# Parallel-netCDF
########################################
rm -rf pnetcdf-1.11.2
tar xzvf ${LIBSRC}/pnetcdf-1.11.2.tar.gz
cd pnetcdf-1.11.2
export CC=$SERIAL_CC
export CXX=$SERIAL_CXX
export F77=$SERIAL_F77
export FC=$SERIAL_FC
export MPICC=$MPI_CC
export MPICXX=$MPI_CXX
export MPIF77=$MPI_F77
export MPIF90=$MPI_FC
export OBJECT_MODE='64'
export CFLAGS='CFLAGS=-D_LARGEFILE64_SOURCE=1 -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE=1 '

./configure --prefix=${LIBBASE} --enable-large-single-req 

make
#make testing
make install

export PNETCDF=${LIBBASE}
cd ..
#rm -rf pnetcdf-1.11.2

########################################
# netCDF (C library)
########################################
rm -rf netcdf-4.6.1
tar xzvf ${LIBSRC}/netcdf-4.6.1.tar.gz
cd netcdf-c-4.6.1
unset  CFLAGS
export CC=$MPI_CC
export MPICC=$MPI_CC
export MPICXX=$MPI_CXX
export MPIF77=$MPI_F77
export MPIF90=$MPI_FC
export CPPFLAGS="-I${LIBBASE}/include"
export LDFLAGS="-L${LIBBASE}/lib"
export LIBS="-lhdf5_hl -lhdf5 -lz -ldl"

./configure --prefix=${LIBBASE} --disable-dap --enable-netcdf4 --enable-pnetcdf --enable-cdf5 --disable-shared --enable-largefile

make
#make check
make install

export NETCDF=${LIBBASE}
cd ..
#rm -rf netcdf-c-4.6.1

########################################
# netCDF (Fortran interface library)
########################################
rm -rf netcdf-fortran-4.4.4
tar xzvf ${LIBSRC}/netcdf-fortran-4.4.4.tar.gz
cd netcdf-fortran-4.4.4

export MPICC=$MPI_CC
export MPICXX=$MPI_CXX
export MPIF77=$MPI_F77
export MPIF90=$MPI_FC
export FC=$MPI_FC
export F77=$MPI_F77
export LIBS="-lnetcdf ${LIBS}"

./configure --prefix=${LIBBASE} --disable-shared --enable-largefile
make
#make check
make install
cd ..
#rm -rf netcdf-fortran-4.4.4


########################################
# PIO
########################################
#rm -rf ParallelIO pio
git clone https://github.com/NCAR/ParallelIO
cd ParallelIO
export PIOSRC=`pwd`
cd ..
mkdir pio
cd pio
export CXX=$SERIAL_CXX
export F77=$SERIAL_F77
export MPICC=$MPI_CC
export MPICXX=$MPI_CXX
export MPIF77=$MPI_F77
export MPIF90=$MPI_FC
export CC=$MPI_CC
export FC=$MPI_FC
unset CFLAGS
export CTEST_OUTPUT_ON_FAILURE=1
cmake -DNetCDF_C_PATH=$NETCDF -DNetCDF_Fortran_PATH=$NETCDF -DPnetCDF_PATH=$PNETCDF -DCMAKE_INSTALL_PREFIX=$LIBBASE -DPIO_USE_MPIIO=ON -DPIO_ENABLE_FORTRAN=ON -DPIO_ENABLE_TIMING=OFF -DPIO_ENABLE_TESTS=OFF -DPIO_ENABLE_LOGGING=OFF -DPIO_USE_MALLOC=ON -DCMAKE_VERBOSE_MAKEFILE=ON $PIOSRC

make install
#make tests
#make check 

cd ..
#rm -rf pio ParallelIO
export PIO=$LIBBASE

########################################
# Other environment vars needed by MPAS
########################################
export MPAS_EXTERNAL_LIBS="-L${LIBBASE}/lib -lhdf5_hl -lhdf5 -ldl -lz"
export MPAS_EXTERNAL_INCLUDES="-I${LIBBASE}/include"
