#!/bin/bash


for i in CCSDT_QZ  CCSDT_TZ B2PLYP_QZ  B2PLYP_TZ  B3LYP  BLYP  BP86  HSE06  PBE  PBE0  SCAN  TPSS  wB97X  wB97X_MRCC
do
	echo ${i}
	for j in perfect defect O
	do
		grep "calc=" ${i}/${j}/MINP
		grep "dft=" ${i}/${j}/MINP
	done
done
