#!/bin/sh
dataset=MAG

cd JointRep/
./run.sh
cd ../

python3 candidate_generation_${dataset}.py
python3 pseudo_label.py
python3 doc_id_${dataset}.py