#!/bin/bash

set -e

for i in TZ QZ
do
        for j in perfect defect
        do
                mkdir -p ${i}/${j}
                cd ${i}/${j}
                cp ../../MINP_Final_${i}_${j} MINP
                cp ../../young_mrcc.sh young_mrcc.sh
                qsub ./young_mrcc.sh
                cd ../../
        done
done

