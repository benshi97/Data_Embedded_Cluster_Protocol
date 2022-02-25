#!/bin/bash -l
#$ -N tio2_b
#$ -l h_rt=48:00:00
#$ -l mem=75G
#$ -l tmpfs=1500G
#$ -pe smp 20
#$ -ac allow=IB
#$ -cwd

export PATH="/home/ucapshi/Programs/orca_5_0_1_linux_x86-64_shared_openmpi411:$PATH"
export LD_LIBRARY_PATH="/home/ucapshi/Programs/orca_5_0_1_linux_x86-64_shared_openmpi411:$LD_LIBRARY_PATH"

export PATH="/home/ucapshi/Programs/openmpi-4.1.1/binary/bin:$PATH"
export LD_LIBRARY_PATH="/home/ucapshi/Programs/openmpi-4.1.1/binary/lib:$LD_LIBRARY_PATH"

WORKDIR=${PWD}

# 9. Run our MPI job. GERun is a wrapper that launches MPI jobs on Legion.
cp $WORKDIR/*.inp $TMPDIR/
cp $WORKDIR/*.gbw $TMPDIR/
cp $WORKDIR/*.xyz $TMPDIR/
cp $WORKDIR/*.hess $TMPDIR/
cp $WORKDIR/*.pc $TMPDIR/
cp $WORKDIR/*.qro $TMPDIR/
cp $WORKDIR/*.bq $TMPDIR/

cd $TMPDIR
/home/ucapshi/Programs/orca_5_0_1_linux_x86-64_shared_openmpi411/orca orca.inp > $WORKDIR/orca.out
cp $TMPDIR/*.gbw $WORKDIR
cp $TMPDIR/*.engrad $WORKDIR
cp $TMPDIR/*.xyz $WORKDIR
cp $TMPDIR/*.loc $WORKDIR
cp $TMPDIR/*.qro $WORKDIR
cp $TMPDIR/*.uno $WORKDIR
cp $TMPDIR/*.unso $WORKDIR
cp $TMPDIR/*.uco $WORKDIR
cp $TMPDIR/*.hess $WORKDIR
cp $TMPDIR/*.cis $WORKDIR
cp $TMPDIR/*.dat $WORKDIR
cp $TMPDIR/*.mp2nat $WORKDIR
cp $TMPDIR/*.nat $WORKDIR
cp $TMPDIR/*.scfp_fod $WORKDIR
cp $TMPDIR/*.scfp $WORKDIR
cp $TMPDIR/*.scfr $WORKDIR
cp $TMPDIR/*.nbo $WORKDIR
cp $TMPDIR/FILE.47 $WORKDIR
cp $TMPDIR/*_property.txt $WORKDIR
cp $TMPDIR/*spin* $WORKDIR
