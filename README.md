# SAC25 Case Study
This repository contains the datasets and scripts for reproducing the experiments that are published in the SAC25 paper.
Particularly, TFG folder contains:
- The daily electricity consumption records of user ID 1153 (day\_\<first_day\>\_\<last_day\>\_user\_\<id\>.zip)
- The timed regular expressions (TXT files)
- The bash-shell and Python scripts for running the evaluation of the TREs against the electricity consumption recordings.

## Installation of dependencies
pip install -r requirements.txt --user

## Digesting several time series into a single probabilistic signal with 95% interval of confidence
In order to summarize the electricity consumption recordings of several days, you can run the following command:

``
python ./signals2prsignal.py ./output_prsignal ./input_signal_1.csv ... ./input_signal_n.csv
``

As output, it will generate a CSV file (named output_prsignal.csv) and a SVG picture (named output_prsignal.svg).
For instance, the next figure shows the average electricity consumption of user ID 1153 in a regular day.
The upper/lower bands are the 95% interval of confidence which includes the 95% of the samples.

![Alt Text](/svg/normal.svg)

You can generate the pictures of SAC 25 paper running the `plot_pictures.sh` script. 
The CSV file contains the time serie information the picture was generated from.
Particularly, it has three columns: 1) the timestamp, 2) the average electricity consumption, and 3) the standard deviation.
As the smart meters register the information every half an hour, the CSV file should consist of 48 entries.

## How to run the experiments
In order to run the experiments, you must firstly install [ParetoLib](https://gricad-gitlab.univ-grenoble-alpes.fr/verimag/tempo/multidimensional_search), version 2.5.1.
Then, you can run the analysis for one of the anomaly scenarios in [fdi50, fdi150, avg, max\_avg, min\_avg, normal, rsa01\_08, rsa2\_5, swap].

``
python experiments.py <attack> ./day_0_50_user_1143/<attack>/days_*
``

For instance, the following command will run the FDI scenario where the data is scaled by 50%.

``
python experiments.py fdi50 ./day_0_50_user_1143/fdi50/days_*
``

As output, the Python script will show the temporal zones that return the execution of the TRE expression agains the electricity consumption record.

![Alt Text](/svg/fdi50.svg)

Additionally, the Python script will overlay the the information of the temporal zones on top of the electricity consumption record.
Green lines represent the time instants when the TRE starts to become true, and the red lines corresponds to the red lines the time instants when the TRE ends. 

![Alt Text](/svg/fdi50.svg)
** Continuar con la explicación **