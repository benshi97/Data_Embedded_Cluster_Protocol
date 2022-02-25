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
		echo "${i} ${j}"
		grep FINAL mrcc.out | tail -n 1 | awk ' { print $4 } '
grep FINAL mrcc.out | tail -n 1 | awk ' { print $4 } ' >> ../../energies_${j}	


		cd ../../
	done
done
