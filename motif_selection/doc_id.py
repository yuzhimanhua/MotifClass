import json
import argparse

parser = argparse.ArgumentParser(description='main', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--dataset', default='mag', choices=['mag', 'amazon'])
args = parser.parse_args()

dataset = args.dataset

paper2id = {}
with open(f'../{dataset}_data/dataset.json') as fin:
	for idx, line in enumerate(fin):
		data = json.loads(line)
		paper2id[data['document']] = str(idx)

with open(f'{dataset}_retrieved_docs.txt') as fin:
	topK = 0
	for line in fin:
		data = line.strip().split()[1:]
		if len(data) > topK:
			topK = len(data)

with open(f'{dataset}_retrieved_docs.txt') as fin, open(f'../text_classification/{dataset}/doc_id.txt', 'w') as fout:
	for idx, line in enumerate(fin):
		fout.write(str(idx)+':')
		data = line.strip().split()[1:]
		papers = [paper2id[x.split('_')[1]] for x in data]
		times = int((topK-1) / len(data)) + 1
		papers = (papers*times)[:topK]
		fout.write(','.join(papers)+'\n')