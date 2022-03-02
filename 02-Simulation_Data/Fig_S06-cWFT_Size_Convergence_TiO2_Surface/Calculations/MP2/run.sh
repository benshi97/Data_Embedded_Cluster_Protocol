#!/bin/bash

set -e

for i in {5..10}
do
	for j in perfect defect
	do
		mkdir -p ${i}/${j}
		cd ${i}/${j}
		cp ../../../${i}/${j}/* .
		cp ../../MINP_LMP2_${i}_${j} MINP
		sed -i 's/SVP/TZVPP/g' MINP
		sed -i 's/scfiguess=small/scfiguess=restart/g' MINP
		cp ../../csd3_mrcc.sh .
		sbatch csd3_mrcc.sh
		cd ../../
	done
done
