#!/bin/bash -l
#$ -N wB97X
#$ -l h_rt=48:00:00
#$ -l mem=40G
#$ -l tmpfs=1500G
#$ -pe smp 36
#$ -ac allow=IB
#$ -cwd

export PATH="/home/ucapshi/Programs/orca_5_0_1_linux_x86-64_shared_openmpi411:$PATH"
export LD_LIBRARY_PATH="/home/ucapshi/Programs/orca_5_0_1_linux_x86-64_shared_openmpi411:$LD_LIBRARY_PATH"

export PATH="/home/ucapshi/Programs/openmpi-4.1.1/binary/bin:$PATH"
export LD_LIBRARY_PATH="/home/ucapshi/Programs/openmpi-4.1.1/binary/lib:$LD_LIBRARY_PATH"


# 9. Run our MPI job. GERun is a wrapper that launches MPI jobs on Legion.
/home/ucapshi/Programs/orca_5_0_1_linux_x86-64_shared_openmpi411/orca orca.inp | tee orca.out orca.out.$JOB_ID
