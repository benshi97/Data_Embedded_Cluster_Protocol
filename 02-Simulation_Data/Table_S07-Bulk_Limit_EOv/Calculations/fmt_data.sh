#!/bin/bash

set -e

touch energies
rm energies*

for i in PBE_MgO_Bulk  PBE_MgO_Surface  PBE_TiO2_Bulk  PBE_TiO2_Surface_2x4  PBE_TiO2_Surface_2x6 PBE0_TiO2_Surface_2x4
do
		cd ${i}
		a=$(grep sigma perfect/OUTCAR | tail -n 1 | awk '{ print $7 }')
		b=$(grep sigma defect/OUTCAR | tail -n 1 | awk '{ print $7 }')
		cd ../
		echo "${i} ${a} ${b}" >> energies_metal-oxide_VASP
done

for i in PBE_O PBE0_O 
do
        cd ${i}
        a=$(grep sigma OUTCAR | tail -n 1 | awk '{ print $7 }')
        cd ../
        echo "${i} ${a}" >> energies_O_VASP
done
