#!/bin/bash

set -e

for i in CCSDT_QZ  CCSDT_TZ B2PLYP_QZ  B2PLYP_TZ  B3LYP  BLYP  BP86  HSE06  PBE  PBE0  SCAN  TPSS
do
	echo ${i}
	for j in perfect defect O
	do
		grep -A 1 "basis=" ${i}/${j}/MINP | tail -n 1
	done
done
