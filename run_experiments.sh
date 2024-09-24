#!/bin/bash
# List of attacks: "avg" "min_avg" "max_avg" "fdi50" "fdi150" "rsa01_08" "rsa2_5" "swap" "normal"
for attack in "avg" "min_avg" "max_avg" "fdi50" "fdi150" "swap" "normal"
do
  python ./experiments.py $attack ./day_0_360_user_1143/$attack/days_*
done

for attack in "rsa01_08" "rsa2_5"
do
  python ./experiments_for_rsa.py $attack ./day_0_360_user_1143/$attack/days_*
done
