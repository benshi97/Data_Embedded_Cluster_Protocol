#!/bin/bash

touch energies
rm energies*

for i in {5..10} # {0..19} #TZVPP
do
	for j in perfect defect
	do
		mkdir -p ${i}/${j}
		cd ${i}/${j}
		echo "${i} ${j}"
		a=$( grep FINAL orca.out | awk '{ print $5 }')
		echo "${i} ${a}" >> ../../energies_${j}_TZVPP


		cd ../../
	done
done
