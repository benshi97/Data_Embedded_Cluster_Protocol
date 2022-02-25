#!/bin/bash
#SBATCH -J mrcc
#SBATCH -A T2-CS146-CPU
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=36:00:00
#SBATCH --mail-type=NONE
#SBATCH --cpus-per-task=76
#SBATCH -p icelake-himem

numnodes=$SLURM_JOB_NUM_NODES
numtasks=$SLURM_NTASKS
. /etc/profile.d/modules.sh                # Leave this line (enables the module command)
module purge                               # Removes all modules still loaded
module load rhel8/default-icl              # REQUIRED - loads the basic environment

export PATH="/home/bxs21/Programs/icelake/mrcc_libxc:$PATH"
export OMP_NUM_THREADS=76
export MKL_NUM_THREADS=76
export OMP_PLACES=cores
export OMP_PROC_BIND=spread,close

/home/bxs21/Programs/icelake/mrcc_libxc/dmrcc MINP | tee mrcc.out mrcc.out.$SLURM_JOB_ID
