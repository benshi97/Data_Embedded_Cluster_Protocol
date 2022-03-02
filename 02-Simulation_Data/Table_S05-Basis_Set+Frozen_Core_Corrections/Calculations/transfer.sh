#!/bin/bash

set -e

for i in TZVPP QZVPP CVTZ CVQZ
do
	for j in perfect defect
	do
		cp orca.bq ${i}/${j}
	done
done
