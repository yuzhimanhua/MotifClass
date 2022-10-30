import json
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser(description='main', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--dataset', default='mag', choices=['mag', 'amazon'])

args = parser.parse_args()
dataset = args.dataset

metadatas = set()
with open(f'../{dataset}_data/motifs.txt') as fin:
	for line in fin:
		data = line.strip().split(',')
		for metadata in data:
			if metadata != 'term':
				metadatas.add(metadata)

label2id = {}
with open(f'../{dataset}_data/labels.txt') as fin:
	for idx, line in enumerate(fin):
		data = line.strip()
		label2id[data] = str(idx)

with open(f'../{dataset}_data/dataset.json') as fin, open(f'{dataset}/dataset.csv', 'w') as fout:
	for idx, line in enumerate(tqdm(fin)):
		data = json.loads(line)
		l_id = label2id[data['label']]
		output = []
		for metadata in metadatas:
			output += [metadata.upper()+'_'+x for x in data[metadata]]
		output = ' '.join(output) + ' ' + data['text']
		fout.write(f'{l_id},{output}\n')