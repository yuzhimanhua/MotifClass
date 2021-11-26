dataset=mag

cd text_classification/

echo "=====Step 1: Dataset Preprocessing====="
python dataset_preprocess.py --dataset ${dataset}

echo "=====Step 2: Pseudo Training Doc Generation and Classifier Training====="
python main.py --dataset ${dataset}
python eval.py --dataset ${dataset}