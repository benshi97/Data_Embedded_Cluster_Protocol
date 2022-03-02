#!/bin/bash -l
#$ -N vasp
#$ -l h_rt=12:00:00
#$ -l mem=4G
#$ -pe mpi 80
#$ -cwd

module unload -f compilers mpi
module load gcc-libs
module load compilers/intel/2019/update5
module load mpi/intel/2019/update5/intel



# 9. Run our MPI job. GERun is a wrapper that launches MPI jobs on Legion.
gerun /home/ucapshi/Programs/vasp.6.2.0/bin/vasp_std >> vasp_output.$JOB_ID
mv INCAR INCAR_SP
cp INCAR_PARCHG INCAR
gerun /home/ucapshi/Programs/vasp.6.2.0/bin/vasp_std >> vasp_output.$JOB_ID
