#!/bin/sh
dataset=$1

threads=5 # number of threads for training
negative=5 # number of negative samples
alpha=0.025 # initial learning rate
sample=10000 # number of training samples (Million)
type=2 # number of edge types
dim=100

word_file="${dataset}_left.dat"
node_file="${dataset}_right.dat"
link_file="${dataset}_network.dat"
emb_file="${dataset}.emb"
kappa_file="${dataset}.kappa"

./bin/jointemb -words ${word_file} -nodes ${node_file} -hin ${link_file} -output ${emb_file} -kappa ${kappa_file} -binary 0 -type ${type} -size ${dim} -negative ${negative} -samples ${sample} -alpha ${alpha} -threads ${threads}