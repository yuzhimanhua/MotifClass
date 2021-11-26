dataset=mag

cd motif_selection/

echo "=====Step 1: Candidate Motif Instance Generation====="
python candidate_generation.py --dataset ${dataset}

echo "=====Step 2: Embedding====="
python embedding_preprocess.py --dataset ${dataset}
./embed.sh ${dataset}
python embedding_postprocess.py --dataset ${dataset}

echo "=====Step 3: Motif Instance Selection====="
python motif_selection.py --dataset ${dataset}

echo "=====Step 4: Pseudo Training Doc Retrieval====="
python retrieve_docs.py --dataset ${dataset}
python doc_id.py --dataset ${dataset}