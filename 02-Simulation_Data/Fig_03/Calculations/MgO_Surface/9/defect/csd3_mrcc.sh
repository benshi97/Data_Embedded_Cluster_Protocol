#!/bin/bash
#SBATCH -J mrcc_mgo
#SBATCH -A T2-CS146-CPU
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=36:00:00
#SBATCH --mail-type=NONE
#SBATCH --cpus-per-task=56
#SBATCH -p cclake

numnodes=$SLURM_JOB_NUM_NODES
numtasks=$SLURM_NTASKS
. /etc/profile.d/modules.sh                # Leave this line (enables the module command)
module purge                               # Removes all modules still loaded
module load rhel7/default-ccl              # REQUIRED - loads the basic environment

export PATH="/home/bxs21/Programs/mrcc_cclake1:$PATH"
export OMP_NUM_THREADS=56
export MKL_NUM_THREADS=56
export OMP_PLACES=cores
export OMP_PROC_BIND=spread,close

/home/bxs21/Programs/mrcc_cclake1/dmrcc | tee mrcc.out mrcc.out.$SLURM_JOB_ID
