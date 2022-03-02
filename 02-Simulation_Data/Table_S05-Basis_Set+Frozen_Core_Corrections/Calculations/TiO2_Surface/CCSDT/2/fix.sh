#!/bin/bash

method='CCSDT'

set -e

for i in CVTZ CVQZ
do
	mv ${i}_Ne ${i}
	cp -r /home/shixubenjamin/Projects/Embedding/Archiving/02-Simulation_Data/Table_S5-Basis_Set+Frozen_Core_Corrections/Calculations/TiO2_Bulk/old/${method}/3/${i}/O ${i}
done

for i in TZVPP QZVPP
do
	mv ${i}_Ar ${i}
	cp -r /home/shixubenjamin/Projects/Embedding/Archiving/02-Simulation_Data/Table_S5-Basis_Set+Frozen_Core_Corrections/Calculations/TiO2_Bulk/old/${method}/3/${i}/O ${i}
done
