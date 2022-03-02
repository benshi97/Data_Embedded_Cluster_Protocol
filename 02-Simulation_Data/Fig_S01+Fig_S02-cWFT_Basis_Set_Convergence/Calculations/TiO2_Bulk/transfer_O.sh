#!/bin/bash

set -e

for i in  CV5Z  CVQZ  CVTZ  QZVPP  SVP  TZVPP  V5Z  VDZ  VQZ  VTZ
do
	cp -r /home/shixubenjamin/Projects/Embedding/Archiving/02-Simulation_Data/Fig_S1/MgO_Surface/Tight/Necore/${i}/O Tight/Arcore/${i}/
	cp -r /home/shixubenjamin/Projects/Embedding/Archiving/02-Simulation_Data/Fig_S1/MgO_Surface/Tight/Necore/${i}/O Tight/Necore/${i}/ 
done
