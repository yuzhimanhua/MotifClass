from collections import defaultdict
import argparse

parser = argparse.ArgumentParser(description='main', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--dataset', default='mag', choices=['mag', 'amazon'])
parser.add_argument('--num_retrieved_docs', default=0, type=int)
args = parser.parse_args()

dataset = args.dataset
motif2paper = {}
with open(f'{dataset}_candidate_motifs.txt') as fin:
	for line in fin:
		data = line.strip().split()
		motif = data[0]
		papers = data[1:]
		motif2paper[motif] = papers

paper2score = defaultdict(lambda: defaultdict(float))
labels = []
with open(f'{dataset}_motifs.txt') as fin:
	for line in fin:
		data = line.strip().split()
		label = data[0][5:]
		labels.append(label)
		for motif in data:
			for paper in motif2paper[motif]:
				paper2score[paper][label] += 1

if args.num_retrieved_docs != 0:
	topK = args.num_retrieved_docs
elif dataset == 'mag':
	topK = 50
elif dataset == 'amazon':
	topK = 100

with open(f'{dataset}_retrieved_docs.txt', 'w') as fout:
	for label in labels:
		scores = {}
		for paper in paper2score:
			if label in paper2score[paper] and len(paper2score[paper]) == 1:
				scores[paper] = paper2score[paper][label]
		scores_sorted = sorted(scores.items(), key=lambda x:x[1], reverse=True)
		fout.write(label)
		for tup in scores_sorted[:topK]:
			fout.write('\t'+tup[0])
		fout.write('\n')