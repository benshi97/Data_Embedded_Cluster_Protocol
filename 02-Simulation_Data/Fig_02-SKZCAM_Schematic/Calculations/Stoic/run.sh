#!/bin/bash

set -e

for i in 3 11 18 26 34 40 50
do
    for j in perfect defect
    do 
        mkdir -p ${i}/${j}
        cd ${i}/${j}
        cp ../../orca.inp_stoic_${i}_${j} orca.inp
        cp ../../orca.bq_stoic_${i} orca.bq
        cp ../../young_orca.sh .
        qsub ./young_orca.sh
        cd ../../
    done
done
