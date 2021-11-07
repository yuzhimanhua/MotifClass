import numpy as np
import argparse

parser = argparse.ArgumentParser(description='main', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--dataset', default='MAG', choices=['MAG', 'Amazon'])

args = parser.parse_args()
dataset = args.dataset
file_path = '../../'

labels = []
with open(file_path+dataset+'_data/labels_new.txt') as fin:
	for line in fin:
		labels.append('TERM_'+line.strip())

label2emb = {}
word2idx = {}
idx2word = {}
word2emb = {}
with open(dataset+'.emb') as fin:
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
with open(dataset+'.kappa') as fin:
	for line in fin:
		data = line.strip().split()
		if len(data) != 2:
			continue
		word = data[0]
		kappa = float(data[1])
		word2kappa[word] = kappa

print(len(word2emb), len(word2kappa), len(label2emb))

embMat = np.zeros((len(idx2word), 100))
for idx in range(len(idx2word)):
	embMat[idx] = word2emb[idx2word[idx]]

topM = 50
min_lambda = 2
with open(dataset+'_motifs.txt', 'w') as fout:
	for label_i, label in enumerate(labels):
		l_emb = word2emb[label]
		res = np.dot(embMat, l_emb)
		idx_sorted = list(np.argsort(-res))

		expanded = []
		k = 0
		kappa_l = word2kappa[label]
		while len(expanded) < topM and k < len(idx_sorted):
			word = idx2word[idx_sorted[k]]
			if word2kappa[word] >= min_lambda*kappa_l:
				motif_new = word.split(',')
				word = ','.join(motif_new)
				expanded.append(word)
			k += 1

		fout.write(label+'\t'+'\t'.join(expanded)+'\n')