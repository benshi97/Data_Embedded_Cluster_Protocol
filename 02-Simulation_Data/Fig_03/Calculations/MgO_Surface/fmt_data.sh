#!/bin/bash

set -e

touch energies
rm energies*

my_array=(4  5  9 17 21 25 29 33 41 42)

for i in {0..9} #TZVPP
do
        for j in perfect defect
        do
                mkdir -p ${i}/${j}
                cd ${i}/${j}
				a=$(grep "FINAL" mrcc.out | tail -n 1 | awk '{ print $4 }')

				b=${my_array[$((${i}))]}
                echo "${b} ${a}" >> ../../energies_${j}_SVP
                cd ../../
        done
done

for i in 3 4 5 #TZVPP
do
        for j in perfect defect
        do
                mkdir -p ${i}_TZVPP/${j}
                cd ${i}_TZVPP/${j}
                a=$(grep "FINAL" mrcc.out | tail -n 1 | awk '{ print $4 }')

                b=${my_array[$((${i}))]}
                echo "${b} ${a}" >> ../../energies_${j}_TZVPP
                cd ../../
        done
done

