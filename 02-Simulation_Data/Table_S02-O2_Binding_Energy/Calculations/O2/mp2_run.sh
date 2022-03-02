#!/bin/bash

set -e

for i in B2PLYP DSDPBEP86 #PBE BP86 BLYP SCAN TPSS PBE0 B3LYP HSE06 # B2PLYP DSDPBEP86
do
        for j in O2 #perfect defect
        do
                for k in TZ QZ
                do
                mkdir -p ${i}_${k}/${j}
                cd ${i}_${k}/${j}
                cp ../../MINP_${i}_${j} MINP
		sed -i "s/L${i}/${i}/g" MINP                
                sed -i 's/rks/uks/g' MINP
		sed -i 's/490GB/170GB/g' MINP	
		sed -i "s/TZVPP/${k}VPP/g" MINP
                cp ../../nest_mrcc.sh .
                sbatch nest_mrcc.sh
                cd ../../
        done
done
done

#for i in B2PLYP DSDPBEP86 #PBE BP86 BLYP SCAN TPSS PBE0 B3LYP HSE06 # B2PLYP DSDPBEP86
#do
#        for j in O1 O2 #perfect defect
#        do
#                for k in TZ QZ
#                do
#                mkdir -p ${i}_${k}/O_${j}
#                cd ${i}_${k}/O_${j}
#                cp ../../MINP_${i}_O2_${j} MINP
#		sed -i "s/L${i}/${i}/g" MINP
#                sed -i 's/rks/uks/g' MINP
#                sed -i 's/490GB/170GB/g' MINP
#                sed -i "s/TZVPP/${k}VPP/g" MINP
#                cp ../../nest_mrcc.sh .
#                sbatch nest_mrcc.sh
#                cd ../../
#        done
#done
#done
#
