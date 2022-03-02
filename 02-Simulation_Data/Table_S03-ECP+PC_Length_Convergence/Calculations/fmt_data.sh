#!/bin/bash

set -e

touch energies
rm energies*

my_array=(2  3  5  7 11 12 16 18 20 22 26 30 32 34 38 40 44)

for i in ECP_7_PC_30 ECP_7_PC_40 ECP_10.6_PC_40 #TZVPP
do
                cd ${i}
				a=$(grep "FINAL" perfect/orca.out | tail -n 1 | awk '{ print $5 }')
				b=$(grep "FINAL" defect/orca.out | tail -n 1 | awk '{ print $5 }')
                echo "${i} ${b} ${a}" >> ../energies_SVP
                cd ../
done

