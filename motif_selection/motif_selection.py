import numpy as np
import argparse

parser = argparse.ArgumentParser(description='main', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--dataset', default='mag', choices=['mag', 'amazon'])
parser.add_argument('--num_motif', default=50, type=int)
parser.add_argument('--eta', default=2.0, type=float)
args = parser.parse_args()

dataset = args.dataset
topM = args.num_motif
eta = args.eta

labels = []
with open(f'../{dataset}_data/labels.txt') as fin:
	for line in fin:
		data = line.strip()
		labels.append('TERM_'+data)

label2emb = {}
word2idx = {}
idx2word = {}
word2emb = {}
with open(f'{dataset}.emb') as fin:
	idx = 0
	for line in fin:
		data = line.strip().split()
		if len(data) != 101:
			continue
		word = data[0]
		emb = np.array([float(x) for x in data[1:]])
		emb = emb / np.linalg.norm(emb)
		word2idx[word] = idx
		idx2word[idx] = word
		word2emb[word] = emb
		idx += 1
		if word in labels:
			label2emb[word] = emb

word2kappa = {}
with open(f'{dataset}.kappa') as fin:
	for line in fin:
		data = line.strip().split()
		if len(data) != 2:
			continue
		word = data[0]
		kappa = float(data[1])
		word2kappa[word] = kappa

embMat = np.zeros((len(idx2word), 100))
for idx in range(len(idx2word)):
	embMat[idx] = word2emb[idx2word[idx]]

with open(f'{dataset}_motifs.txt', 'w') as fout:
	for label in labels:
		l_emb = word2emb[label]
		res = np.dot(embMat, l_emb)
		idx_sorted = list(np.argsort(-res))

		expanded = []
		k = 0
		kappa_l = word2kappa[label]
		while len(expanded) < topM and k < len(idx_sorted):
			word = idx2word[idx_sorted[k]]
			if word2kappa[word] >= eta*kappa_l:
				expanded.append(word)
			k += 1

		fout.write(label+'\t'+'\t'.join(expanded)+'\n')