#!/bin/bash

set -e

for i in CVTZ CVQZ TZVPP QZVPP
do
	echo ${i}
	for j in perfect defect O
	do
		grep -A 1 "basis=" ${i}/${j}/MINP | tail -n 1
	done
done
