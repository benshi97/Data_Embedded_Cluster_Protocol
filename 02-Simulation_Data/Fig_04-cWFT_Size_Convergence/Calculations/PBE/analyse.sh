#!/bin/bash

set -e

touch energies
rm energies*

for i in {5..10} #TZVPP
do
	for j in perfect defect
	do
		mkdir -p ${i}/${j}
		cd ${i}/${j}
		echo "${i} ${j}"
		
		if  grep "FINAL KOHN" mrcc.out | sed -n '2 p'| grep -q "FINAL KOHN"; then
			a=$(grep "FINAL KOHN" mrcc.out | tail -n 1 | awk '{ print $4 }')
		else
			a=0
		fi
		echo "${i} ${a}" >> ../../energies_${j}
		cd ../../
	done
done
