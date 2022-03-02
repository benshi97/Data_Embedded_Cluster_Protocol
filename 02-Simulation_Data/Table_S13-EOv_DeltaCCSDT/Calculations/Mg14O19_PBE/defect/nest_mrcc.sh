#!/bin/bash
#SBATCH -J mrcc
#SBATCH -p MAIN
#SBATCH --time=48:00:0
#SBATCH -N1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=40

export OMP_NUM_THREADS=40
export MKL_NUM_THREADS=40
export PATH="/home/bxs21/Programs/mrcc_libxc:$PATH"

WORKDIR=$PWD
/home/bxs21/Programs/mrcc_libxc/dmrcc MINP | tee mrcc.out mrcc.out.$SLURM_JOB_ID
