#!/bin/bash

set -e

for i in {0..5}
do
	rsync -zarv --include="*/" --include="*MINP*" --include="mrcc.out" --include="*.sh" --include="orca.inp" --include="orca.out" --include="orca.bq" --exclude="*" icepc03:/home/bxs21/Scratch/Projects/Embedding/Calculations/22_01_19-Ti3_Permutations_Stoic/TZVPP/${i}/ 3_${i}
done
