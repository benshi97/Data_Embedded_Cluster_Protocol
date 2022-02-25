#!/bin/bash
set -e

touch energies
rm energies*

my_array=(4  5  9 17 21 25 29 33 41 42)

for i in {0..9}
do
	for j in perfect defect
	do
		mkdir -p ${i}/${j}
		cd ${i}/${j}
		echo "${i} ${j}"
		a=$(grep "Total LNO-CCSD(T) energy with MP2 corrections" mrcc.out | tail -n 1 | awk ' { print $8 } ')
		b=$(grep "Total LMP2 energy" mrcc.out | tail -n 1 | awk ' { print $5 } ')
		c=$(grep "Reference energy" mrcc.out | tail -n 1 | awk ' { print $4 } ')
		echo "${my_array[$((${i}))]} ${a} ${b} ${c}" >> ../../energies_${j}_TZVPP
		cd ../../
	done
done
