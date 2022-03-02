#!/bin/bash

set -e


rsync -zarv  --include "*/" --include="*.out" --include="MINP" --exclude="*" csd3:/home/bxs21/rds/rds-t2-cs146-0QSA3yUapwI/bxs21/Embedding/21_12_02-FINAL-CBS_Conv_MgO+TiO2/MgO_Surface/ .


#rsync -zarv  --include "*/" --include="*.out" --include="MINP" --exclude="*" nest:/home/bxs21/Scratch/CBS_Convergence/O/sorted_data/ .
