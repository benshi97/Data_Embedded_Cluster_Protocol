#!/bin/bash

set -e

touch energies
rm energies*

my_array=(2  4  5  7 11 13 17 21 25 29 31 33 35 37 41 45)

for i in {0..15} #TZVPP
do
        for j in perfect defect
        do
                mkdir -p ${i}/${j}
                cd ${i}/${j}
				a=$(grep "FINAL" mrcc.out | tail -n 1 | awk '{ print $4 }')

				b=${my_array[$((${i}))]}
                echo "${b} ${a}" >> ../../energies_${j}_TZVPP
                cd ../../
        done
done

