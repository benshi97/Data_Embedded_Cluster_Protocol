#!/bin/bash

set -e

touch energies
rm energies*

my_array=(14 16 18 22 26 30)
counter=0
for i in {5..10} #TZVPP
do

        for j in perfect defect
        do
                mkdir -p ${i}/${j}
                cd ${i}/${j}
				a=$(grep "FINAL" mrcc.out | tail -n 1 | awk '{ print $4 }')

				b=${my_array[$((${counter}))]}
                echo "${b} ${a}" >> ../../energies_${j}_TZVPP
                cd ../../
        done
	counter=$(($counter +1))
done

