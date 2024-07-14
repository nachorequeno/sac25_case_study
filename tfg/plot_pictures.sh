#!/bin/bash
for attack in "avg" "min_avg" "max_avg" "fdi50" "fdi150" "rsa01_08" "rsa2_5" "swap" "normal"
do
	#ls -l day_0_50_user_1143/$attack/*csv
	python ../signals2prsignal/signals2prsignal.py $attack  day_0_360_user_1143/$attack/*csv
done
