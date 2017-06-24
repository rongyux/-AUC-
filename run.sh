#!/bin/bash
set -e
set -x
cat do-pre-data/in.dat | python calcu_AUC_Qdistribution.py > out.dat
