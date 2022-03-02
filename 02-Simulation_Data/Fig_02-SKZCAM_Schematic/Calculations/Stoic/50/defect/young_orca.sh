#!/bin/bash -l
#$ -N orca
#$ -l h_rt=24:00:00
#$ -P Gold
#$ -A UKCP_CAM_C
#$ -l mem=23G
#$ -pe mpi 16
#$ -ac allow=C
#$ -cwd

export PATH="/home/mmm0606/Programs/orca_5_0_1_linux_x86-64_shared_openmpi411:$PATH"
export LD_LIBRARY_PATH="/home/mmm0606/Programs/orca_5_0_1_linux_x86-64_shared_openmpi411:$LD_LIBRARY_PATH"

export PATH="/home/mmm0606/Programs/openmpi-4.1.1/binary/bin:$PATH"
export LD_LIBRARY_PATH="/home/mmm0606/Programs/openmpi-4.1.1/binary/lib:$LD_LIBRARY_PATH"


# 9. Run our MPI job. GERun is a wrapper that launches MPI jobs on Legion.
/home/mmm0606/Programs/orca_5_0_1_linux_x86-64_shared_openmpi411/orca orca.inp > orca.out
