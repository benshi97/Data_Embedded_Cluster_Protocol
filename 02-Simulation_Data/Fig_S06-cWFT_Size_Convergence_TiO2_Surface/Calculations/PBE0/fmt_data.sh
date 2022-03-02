#!/bin/bash

set -e

touch energies
rm energies*

for i in {5..10} #TZVPP
do
		cd ${i}
		
		a=$(grep "FINAL KOHN" perfect/mrcc.out | tail -n 1 | awk '{ print $4 }')
		b=$(grep "FINAL KOHN" defect/mrcc.out | tail -n 1 | awk '{ print $4 }')
		echo "${i} ${a} ${b}" >> ../energies_TZVPP
		cd ../
done
