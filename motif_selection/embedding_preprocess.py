import json
from collections import defaultdict
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser(description='main', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--dataset', default='mag', choices=['mag', 'amazon'])
parser.add_argument('--window', default=5, type=int)
args = parser.parse_args()

dataset = args.dataset
window = args.window
left = set()
right = set()
with open(f'{dataset}_network.dat', 'w') as fout:
	# Motif-Document
	with open(f'{dataset}_candidate_motifs.txt') as fin:
		for line in fin:
			data = line.strip().split()
			motif = data[0]
			left.add(motif)
			for paper in data[1:]:
				right.add(paper)
				fout.write(motif+' '+paper+' 0 1\n')

	# Motif (Term)-Context
	with open(f'../{dataset}_data/dataset.json') as fin:
		for idx, line in enumerate(tqdm(fin)):
			data = json.loads(line)

			seq = []
			for x in data['text'].split():
				motif = 'TERM_'+x
				if motif in left:
					seq.append(motif)
			for i in range(len(seq)):
				for j in range(i-window, i+window+1):
					if j < 0 or j >= len(seq) or j == i:
						continue
					right.add(seq[j])
					fout.write(seq[i]+' '+seq[j]+' 1 1\n')
				
with open(f'{dataset}_left.dat', 'w') as fou1, open(f'{dataset}_right.dat', 'w') as fou2:
	for x in left:
		fou1.write(x+'\n')
	for x in right:
		fou2.write(x+'\n')