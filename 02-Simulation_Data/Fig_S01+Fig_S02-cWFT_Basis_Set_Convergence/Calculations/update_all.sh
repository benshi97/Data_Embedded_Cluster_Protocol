#!/bin/bash

set -e

for i in TiO2_Surface #MgO_Bulk MgO_Surface TiO2_Bulk
do
	cd ${i}
	./transfer.sh
	cd ../
done
