#!/bin/bash

set -e

for i in PBE BP86 BLYP SCAN TPSS PBE0 B3LYP HSE06 # B2PLYP DSDPBEP86
do
        for j in O
        do
                mkdir -p ${i}/${j}
                cd ${i}/${j}
                cp ../../MINP_${i}_${j} MINP
                sed -i 's/rks/uks/g' MINP
		sed -i 's/TZVPP/QZVPP/g' MINP
                sed -i 's/490GB/170GB/g' MINP
		cp ../../nest_mrcc.sh .
                sbatch nest_mrcc.sh
                cd ../../
        done
done

