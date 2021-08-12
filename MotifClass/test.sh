dataset=mag
sup_source=docs
model=cnn
embedding=joint

python3 main.py --dataset ${dataset} --sup_source ${sup_source} --model ${model} --embedding ${embedding} --alpha 0
python3 eval.py --dataset ${dataset}
