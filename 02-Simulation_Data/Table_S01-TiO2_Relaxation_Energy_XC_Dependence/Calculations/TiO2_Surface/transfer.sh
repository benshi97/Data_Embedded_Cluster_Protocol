#!/bin/bash

set -e

for i in LDA PBE PBEsol SCAN
do

	rsync -zarv --include="*/" --include="OUTCAR" --include="*MINP*" --include="INCAR" --include="KPOINTS" --include="POTCAR" --include="POSCAR" --include="CONTCAR" --include="mrcc.out" --include="*.sh" --include="orca.inp" --include="orca.out" --include="orca.bq" --exclude="*" kathleen:/home/ucapshi/Scratch/Embedding/21_07_07-FINAL-Functional_Compare_Relax_Energy_TiO2_Surf/relaxation_energy/${i}/${i}/{defect,defect_unrelaxed} ${i}

done
