dataset=mag

green=`tput setaf 2`
reset=`tput sgr0`

cd text_classification/

echo "${green}=====Step 1: Dataset Preprocessing=====${reset}"
python dataset_preprocess.py --dataset ${dataset}

echo "${green}=====Step 2: Pseudo Training Doc Generation and Classifier Training=====${reset}"
python main.py --dataset ${dataset}
python eval.py --dataset ${dataset}