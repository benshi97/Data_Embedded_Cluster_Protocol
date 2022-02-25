#!/bin/bash
#SBATCH -J mrcc
#SBATCH -p CLUSTER
#SBATCH --time=168:00:0
#SBATCH -N1
#SBATCH --tasks-per-node=1
#SBATCH --cpus-per-task=40

export OMP_NUM_THREADS=40
export MKL_NUM_THREADS=40
export PATH="/home/bxs21/Programs/mrcc_libxc:$PATH"

WORKDIR=$PWD
mkdir -p /scratch/bxs21/$SLURM_JOB_ID
TMPDIR="/scratch/bxs21/$SLURM_JOB_ID"
cd $TMPDIR
cp $WORKDIR/* .
/home/bxs21/Programs/mrcc_libxc/dmrcc MINP | tee $WORKDIR/mrcc.out $WORKDIR/mrcc.out.$SLURM_JOB_ID ./mrcc.out ./mrcc.out.$SLURM_JOB_ID
