#!/bin/bash

set -e

touch energies
rm energies*

my_array=(2  3  5  7 11 12 16 18 20 22 26 30 32 34 38 40 44)

        for j in perfect defect
        do
                mkdir -p ${j}
                cd ${j}
				a=$(grep "FINAL" mrcc.out | tail -n 1 | awk '{ print $4 }')

				#b=${my_array[$((${i}))]}
                echo "18 ${a}" >> ../energies_${j}_TZVPP
                cd ../
done

