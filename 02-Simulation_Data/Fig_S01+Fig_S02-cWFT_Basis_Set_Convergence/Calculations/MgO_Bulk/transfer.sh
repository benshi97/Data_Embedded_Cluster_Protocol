#!/bin/bash

set -e

rsync -zarv  --include "*/" --include="*.out" --include="MINP" --exclude="*" nest:/home/bxs21/Scratch/CBS_Convergence/MgO_Bulk/ .

rsync -zarv  --include "*/" --include="*.out" --include="MINP" --exclude="*" csd3:/rds/project/rds-0QSA3yUapwI/bxs21/CBS_Convergence/MgO_Bulk/ .

rsync -zarv  --include "*/" --include="*.out" --include="MINP" --exclude="*" nest:/home/bxs21/Scratch/CBS_Convergence/O/sorted_data/ .
