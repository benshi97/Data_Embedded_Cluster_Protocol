#!/bin/bash

set -e

touch energies
rm energies*

for i in TiO2_Surface TiO2_Bulk
do
		for j in LDA PBE PBEsol R2SCAN
		do
		cd ${i}/${j}
		a=$(grep sigma defect/OUTCAR | tail -n 1 | awk '{ print $7 }')
		b=$(grep sigma defect_unrelaxed/OUTCAR | tail -n 1 | awk '{ print $7 }')
		cd ../../
		echo "${j} ${a} ${b}" >> energies_${i}
		done
done

