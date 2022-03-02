#!/bin/bash

touch energies
rm energies*


for i in 1  #3 5 7 #9 #11
do
	for j in 2 #3 # 4 5 6 7 8 9 10 11
	do
		for k in 2 3 4 5 #1 2  #4 5 6 7 8
		do
				cd ${i}_${j}_${k}
				unset a b c d		
				a=0
				b=0
				c=0
				d=0
				a=$(grep "Ti " perfect/orca.inp | wc -l)
				b=$(grep "O " perfect/orca.inp | wc -l)
				c=$(grep FINAL perfect/orca.out | awk ' { print $5 } ')
				d=$(grep FINAL defect/orca.out | awk ' { print $5 } ')
				echo "${i} ${j} ${k} ${a} ${b} ${c} ${d}" >> ../energies_SVP

				cd ../
		done
	done
done
