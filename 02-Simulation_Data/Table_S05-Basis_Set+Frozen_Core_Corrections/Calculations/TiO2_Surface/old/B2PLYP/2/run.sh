#!/bin/bash


for i in CVQZ_Ne  CVTZ_Ne  TZVPP_Ar QZVPP_Ar 
do
	cd ${i}/O
	sed -i 's/DLPNO-CCSD(T)/DLPNO-B2PLYP/g' orca.inp     
      	sed -i 's/Method HF/ Method DFT/g' orca.inp
	sed -i 's/HFTyp uhf/HFTyp uks/g' orca.inp	
	/home/bxs21/Programs/Final/orca/orca orca.inp > orca.out
	cd ../../
done
