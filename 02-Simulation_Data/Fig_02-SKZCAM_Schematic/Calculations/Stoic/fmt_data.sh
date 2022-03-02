#!/bin/bash
set -e

touch energies
rm energies*

for i in 11 18 26 34 40 50
do
    for j in perfect defect
    do 
        mkdir -p ${i}/${j}
        cd ${i}/${j}
        a=$(grep FINAL orca.out | tail -n 1 | awk ' { print $5 }')
		echo "${i} ${a}" >> ../../energies_${j}_TZVPP
        
        cd ../../
    done
done

for i in {0..5}
do
	for j in perfect defect
	    do
        cd 3/3_${i}/${j}
        a=$(grep FINAL orca.out | tail -n 1 | awk ' { print $5 }')
        echo "${i} ${a}" >> ../../../energies_Ti3_configurations_${j}_TZVPP

        cd ../../../
    done
done
