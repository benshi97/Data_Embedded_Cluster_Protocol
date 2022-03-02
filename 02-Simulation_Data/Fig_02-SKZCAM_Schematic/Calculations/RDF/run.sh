#!/bin/bash
set -e

for i in {0..16} #9 10 11 #2 3 #{0..5}
do
	for j in perfect defect
	do
		mkdir -p ${i}/${j}
		cd ${i}/${j}
		#cp ../../../pbe0/${i}/${j}/* .
		#cp ../../../${i}/${j}/MINP .
		#sed -i 's/SVP/TZVPP/g' MINP
		#sed -i 's/scfiguess=sad/scfiguess=restart/g' MINP
#		
		cp ../../csd3_mrcc.sh .
		sbatch csd3_mrcc.sh
		cd ../../
	done
done
