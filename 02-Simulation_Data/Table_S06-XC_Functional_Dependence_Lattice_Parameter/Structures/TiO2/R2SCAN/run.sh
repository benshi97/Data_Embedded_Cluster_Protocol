#!/bin/bash

set -e

cp CONTCAR POSCAR_1
cp CONTCAR POSCAR
qsub ./kathleen_vasp.sh
