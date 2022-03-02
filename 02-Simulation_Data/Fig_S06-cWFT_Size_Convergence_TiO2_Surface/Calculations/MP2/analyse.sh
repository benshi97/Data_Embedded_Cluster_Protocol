#!/bin/bash

set -e

touch energies
rm energies*

for i in {5..10}
do

	for j in perfect defect
	do
		mkdir -p ${i}/${j}
		cd ${i}/${j}
		grep "ECP" mrcc.out | tail -n 1
		grep "DF-MP2 energy" mrcc.out | awk ' { print $4 } ' >> ../../energies_MP2_${j}
	       	grep "Reference energy" mrcc.out | awk ' { print $4 } ' >> ../../energies_HF_${j}	


		cd ../../
	done
done
