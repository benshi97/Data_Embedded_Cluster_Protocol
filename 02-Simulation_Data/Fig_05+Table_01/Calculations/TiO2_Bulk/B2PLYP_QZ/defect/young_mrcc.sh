#!/bin/bash -l
#$ -N orca
#$ -l h_rt=96:00:00
#$ -P GoldLong
#$ -A UKCP_CAM_C
#$ -l mem=80G
#$ -pe smp 36
#$ -ac allow=Z
#$ -cwd

module load libxc

WORKDIR=${PWD}

export PATH="/home/mmm0606/Programs/mrcc_libxc:$PATH"

# 9. Run our MPI job. GERun is a wrapper that launches MPI jobs on Legion.
/home/mmm0606/Programs/mrcc_libxc/dmrcc MINP | tee mrcc.out mrcc.out.$JOB_ID
