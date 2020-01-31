#!/bin/bash
 nodes=(50 60)
 p=(0.3 0.35)
 # shellcheck disable=SC2068
 for i in ${nodes[@]};
 do
   for ps in ${p[@]};
   do
   python3 main.py --nodes $i --p $ps  >> results.txt
   done
done