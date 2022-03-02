#!/bin/bash

# Request 16 nodes (1024 MPI tasks at 64 tasks per node) for 3 hours
# Note setting --cpus-per-task=2 to distribute the MPI tasks evenly
# across the NUMA regions on the node   

#SBATCH --job-name=tio2_slab
#SBATCH --nodes=8
#SBATCH --tasks-per-node=64
#SBATCH --cpus-per-task=2
#SBATCH --time=48:00:00

# Replace [budget code] below with your project code (e.g. t01)
#SBATCH --account=e89-camc
#SBATCH --partition=standard
#SBATCH --qos=long

# Setup the job environment (this module needs to be loaded before any other modules)
module load epcc-job-env

# Load the VASP module, avoid any unintentional OpenMP threading by
# setting OMP_NUM_THREADS, and launch the code.
export OMP_NUM_THREADS=1
module load vasp/6
cp WAVECAR WAVECAR_$SLURM_JOB_ID
srun --distribution=block:block --hint=nomultithread vasp_std
