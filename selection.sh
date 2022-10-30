dataset=mag

green=`tput setaf 2`
reset=`tput sgr0`

cd motif_selection/

echo "${green}=====Step 1: Candidate Motif Instance Generation=====${reset}"
python candidate_generation.py --dataset ${dataset}

echo "${green}=====Step 2: Embedding=====${reset}"
python embedding_preprocess.py --dataset ${dataset}
./embed.sh ${dataset}
python embedding_postprocess.py --dataset ${dataset}

echo "${green}=====Step 3: Motif Instance Selection=====${reset}"
python motif_selection.py --dataset ${dataset}

echo "${green}=====Step 4: Pseudo Training Doc Retrieval=====${reset}"
python retrieve_docs.py --dataset ${dataset}
python doc_id.py --dataset ${dataset}