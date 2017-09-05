#!/bin/bash

date > output.txt
python tournament_MNDCvsI.py >> output.txt
date >> output.txt
python tournament_IDOvsI.py >> output.txt
date >> output.txt
python tournament_INDCvsI.py >> output.txt
date >> output.txt
python tournament_MDOvsI.py >> output.txt
date >> output.txt
