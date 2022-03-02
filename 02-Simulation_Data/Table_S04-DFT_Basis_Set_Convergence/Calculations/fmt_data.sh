#!/bin/bash

touch energies
rm energies*

set -e

for i in MgO_Bulk MgO_Surface TiO2_Bulk TiO2_Surface
do
	for j in PBE PBE0
	do
		a=$(grep "FINAL KOHN" ${i}/${j}/perfect/mrcc.out | tail -n 1 | awk ' { print $4 } ')
		b=$(grep "FINAL KOHN" ${i}/${j}/defect/mrcc.out | tail -n 1 | awk ' { print $4 } ')
 		c=$(grep "FINAL KOHN" ${i}/${j}/perfect/mrcc.out | head -n 1 | awk ' { print $4 } ')
        d=$(grep "FINAL KOHN" ${i}/${j}/defect/mrcc.out | head -n 1 | awk ' { print $4 } ')
		echo "${a} ${b}" >> energies_${j}_TZVPP
		echo "${c} ${d}" >> energies_${j}_SVP
	done
done	
