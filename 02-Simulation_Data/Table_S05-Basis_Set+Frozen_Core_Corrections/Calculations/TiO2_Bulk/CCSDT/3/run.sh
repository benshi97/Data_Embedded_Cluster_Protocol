#!/bin/bash

set -e

        for j in CVTZ_Ne CVQZ_Ne TZVPP_Ar QZVPP_Ar #VDZ VTZ VQZ V5Z CVDZ CVTZ CVQZ CV5Z SVP TZVPP QZVPP
        do
                for k in perfect defect
                do
                        mkdir -p ${j}/${k}
                        cd ${j}/${k}
                        cp ../../MINP_${j}_${k} MINP
                        cp ../../csd3_mrcc.sh .
                        sbatch csd3_mrcc.sh
                        cd ../../
		done
                done

