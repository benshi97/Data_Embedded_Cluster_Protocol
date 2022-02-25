#!/bin/bash

set -e

for i in CVTZ CVQZ TZVPP QZVPP
do
	echo ${i}
	for j in perfect defect O
	do
		grep -A 2 "basis" ${i}/${j}/orca.inp
	done
done
