#!/bin/bash
set -e

touch energies
rm energies*

my_array=(6  14  38  68  92 116)

for i in {0..3}
do
	for j in perfect defect
	do
		mkdir -p ${i}/${j}
		cd ${i}/${j}
		echo "${i} ${j}"
		grep "DF-MP2 energy" mrcc.out | tail -n 1 | awk ' { print $4 } '
		a=$(grep "DF-MP2 energy" mrcc.out | tail -n 1 | awk ' { print $4 } ')
		echo "${my_array[$((${i}))]} ${a}" >> ../../energies_${j}_TZVPP	

		cd ../../
	done
done
