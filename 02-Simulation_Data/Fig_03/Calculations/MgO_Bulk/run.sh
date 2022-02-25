#!/bin/bash
set -e

for i in {0..5}
do
	for j in perfect defect
	do
		mkdir -p ${i}/${j}
		cd ${i}/${j}
		cp ../../MINP_rdf_${i}_${j} MINP
		cp ../../csd3_mrcc.sh .
		sed -i 's/delta/nothing/g' MINP
		sbatch csd3_mrcc.sh
		cd ../../
	done
done
