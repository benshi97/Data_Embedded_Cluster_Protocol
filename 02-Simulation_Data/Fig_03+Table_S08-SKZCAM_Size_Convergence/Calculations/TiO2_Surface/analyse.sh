#!/bin/bash

set -e

touch energies
rm energies*

for i in {0..15} #TZVPP
do
	for j in perfect defect
	do
		mkdir -p ${i}/${j}
		cd ${i}/${j}
		echo "${i} ${j}"
		
		if grep -q "FINAL KOHN" mrcc.out ; then
			a=$(grep "FINAL KOHN" mrcc.out | tail -n 1 | awk '{ print $4 }')
		else
			a=0
		fi
		echo "${i} ${a}" >> ../../energies_${j}_surface_TZVPP
		cd ../../
	done
done
