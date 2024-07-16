# Installation of dependencies
pip install -r requirements.txt --user

# Digesting several time series into a single probabilistic signal with 95% interval of confidence
In order to summarize the electricity consumption recordings of several days, you can run the following command:

``
python ./signals2prsignal.py ./output_prsignal ./input_signal_1.csv ... ./input_signal_n.csv
``

As output, it will generate a CSV file (named output_prsignal.csv) and a SVG picture (named output_prsignal.svg).
For instance, the next figure shows the average electricity consumption of user ID 1153 in a regular day.
The upper/lower bands are the 95% interval of confidence which includes the 95% of the samples.

![Alt Text](tfg/svg/normal.svg)

You can generate the pictures of SAC 25 paper running the `plot_pictures.sh` script. 
The CSV file contains the time series information the picture was generated from.
Particularly, it has three columns: 1) the timestamp, 2) the average electricity consumption, and 3) the standard deviation.
As the smart meters register the information every half an hour, the CSV file should consist of 48 entries.