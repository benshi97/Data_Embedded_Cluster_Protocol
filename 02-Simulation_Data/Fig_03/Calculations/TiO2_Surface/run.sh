#!/bin/bash

set -e

for i in {0..15} #TZVPP
do
	for j in perfect defect
	do
		mkdir -p ${i}/${j}
		cd ${i}/${j}
		#cp ../../../${i}/${j}/* .
		sed -i 's/scfiguess=small/scfiguess=restart/g' MINP
		sed -i 's/SVP/TZVPP/g' MINP
		sbatch csd3_mrcc.sh
		cd ../../
	done
done
