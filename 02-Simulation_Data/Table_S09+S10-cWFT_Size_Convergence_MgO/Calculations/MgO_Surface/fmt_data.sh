#!/bin/bash
set -e

touch energies
rm energies*

for i in {0..9}
do
	for j in perfect defect
	do
		mkdir -p ${i}/${j}
		cd ${i}/${j}
		a=$(grep "Total LNO-CCSD(T) energy with MP2 corrections" mrcc.out | tail -n 1 | awk ' { print $8 } ')
		b=$(grep "Total LMP2 energy" mrcc.out | tail -n 1 | awk ' { print $5 } ')
		echo "${i} ${a} ${b}" >> ../../energies_${j}_TZVPP
		cd ../../
	done
done
