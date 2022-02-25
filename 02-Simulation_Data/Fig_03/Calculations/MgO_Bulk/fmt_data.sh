#!/bin/bash

set -e

touch energies
rm energies*

my_array=(6  14  38  68  92 116)

for i in {0..5} #TZVPP
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

for i in 2 3 #TZVPP
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

