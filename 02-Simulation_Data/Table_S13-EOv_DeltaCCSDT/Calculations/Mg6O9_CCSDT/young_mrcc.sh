#!/bin/bash -l
#$ -N Richter
#$ -l h_rt=10:00:00
#$ -l mem=5G
#$ -l tmpfs=1500G
#$ -pe smp 36
#$ -ac allow=HD
#$ -cwd

export PATH="/home/ucapshi/Programs/libxc_4/test:$PATH"



# 9. Run our MPI job. GERun is a wrapper that launches MPI jobs on Legion.
/home/ucapshi/Programs/libxc_4/test/dmrcc MINP | tee mrcc.out mrcc.out.$JOB_ID
