from collections import defaultdict
import argparse

parser = argparse.ArgumentParser(description='main', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--dataset', default='MAG', choices=['MAG', 'Amazon'])

args = parser.parse_args()
dataset = args.dataset
method = 'JointRep'

motif2paper = {}
print('Reading Matching Network...')
with open(dataset+'_motif_matching.txt') as fin:
	for line in fin:
		data = line.strip().split()
		motif = data[0]
		papers = data[1:]
		motif2paper[motif] = papers

paper2score = defaultdict(lambda: defaultdict(float))
labels = []
topM = 50
print('Reading Motifs...')
with open(method+'/'+dataset+'_motifs.txt') as fin:
	for line in fin:
		data = line.strip().split()
		label = data[0][5:]
		labels.append(label)
		
		motifs = data[:topM]
		for motif in motifs:
			for paper in motif2paper[motif]:
				paper2score[paper][label] += 1

topKs = [50, 100, 200, 1000]
print('Sorting and Output...')
for topK in topKs:
	with open(dataset+'_'+method.lower()+'_'+str(topK)+'.txt', 'w') as fout:
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