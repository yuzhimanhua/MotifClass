import json
from collections import defaultdict
from collections import deque
import argparse
from tqdm import tqdm

parser = argparse.ArgumentParser(description='main', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--dataset', default='mag', choices=['mag', 'amazon'])
parser.add_argument('--min_count', default=5, type=int)
args = parser.parse_args()
dataset = args.dataset

motifs = []
with open(f'../{dataset}_data/motifs.txt') as fin:
	for line in fin:
		if 'term' not in line:
			data = line.strip().split(',')
			motifs.append(data)

motif2paper = defaultdict(list)
with open(f'../{dataset}_data/dataset.json') as fin:
	for idx, line in enumerate(tqdm(fin)):
		data = json.loads(line)
		D = 'DOCUMENT_'+data['document']
		
		# Metadata Motif Instances
		for motif in motifs:
			max_l = len(motif)
			Q = deque()
			metadata = motif[0]
			for x in data[metadata]:
				M = metadata.upper()+'_'+x.replace(' ', '_')
				Q.append(M)
			while Q:
				M = Q.popleft()
				ms = M.split(',')
				l = len(ms)
				if l == max_l:
					motif2paper[M].append(D)
					continue
				metadata = motif[l]
				for x in data[metadata]:
					m_new = metadata.upper()+'_'+x.replace(' ', '_')
					can_add = 1
					for m in ms:
						if m.startswith(metadata.upper()+'_') and m_new <= m:
							can_add = 0
							break
					if can_add == 1:
						M_new = M+','+m_new
						Q.append(M_new)

		# Term Instances
		for x in data['text'].split():
			M = 'TERM_'+x
			motif2paper[M].append(D)

min_count = args.min_count
with open(f'{dataset}_candidate_motifs.txt', 'w') as fout:
	for motif in motif2paper:
		if len(motif2paper[motif]) >= min_count:
			fout.write(motif+'\t'+' '.join(motif2paper[motif])+'\n')
