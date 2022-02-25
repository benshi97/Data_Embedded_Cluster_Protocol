#!/bin/bash

set -e

touch energies
rm energies*

for i in {0..10} #TZVPP
do
        for j in perfect defect
        do
                mkdir -p ${i}/${j}
                cd ${i}/${j}
				a=$(grep "FINAL" orca.out | tail -n 1 | awk '{ print $5 }')

				b=$(grep "Ti " orca.inp | wc -l) #${my_array[$((${i}))]}
                echo "${b} ${a}" >> ../../energies_${j}_SVP
                cd ../../
        done
done

