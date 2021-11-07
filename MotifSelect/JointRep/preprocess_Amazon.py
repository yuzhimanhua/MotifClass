import json
from collections import defaultdict
import argparse

dataset = 'Amazon'
file_path = '../../'

motif2paper = defaultdict(list)
with open(file_path+dataset+'_data/'+dataset+'_clean_new.json') as fin:
	for idx, line in enumerate(fin):
		if idx % 10000 == 0:
			print(idx)
		js = json.loads(line)
		D = 'DOCUMENT_'+js['id']
		
		# User
		U = js['user'][0]
		motif = 'USER_'+U
		motif2paper[motif].append(D)

		# Product
		P = js['product'][0]
		motif = 'PRODUCT_'+P
		motif2paper[motif].append(D)

		# User-Product
		motif = 'USER_'+U+','+'PRODUCT_'+P
		motif2paper[motif].append(D)

		# Term
		for T in js['text'].split():
			motif = 'TERM_'+T
			motif2paper[motif].append(D)

left = set()
right = set()
min_count = 5
win = 5
with open(dataset+'/network.dat', 'w') as fout:
	# Motif-Paper
	for motif in motif2paper:
		if len(motif.split()) >= 2:
			print(motif)
		if len(motif2paper[motif]) >= min_count:
			left.add(motif)
			for paper in motif2paper[motif]:
				right.add(paper)
				fout.write(motif+' '+paper+' 0 1\n')

	# Motif (Term)-Context
	with open(file_path+dataset+'_data/'+dataset+'_clean_new.json') as fin:
		for idx, line in enumerate(fin):
			if idx % 10000 == 0:
				print(idx)
			js = json.loads(line)

			seq = []
			for T in js['text'].split():
				motif = 'TERM_'+T
				if len(motif2paper[motif]) >= min_count:
					seq.append(motif)
			for i in range(len(seq)):
				for j in range(i-win, i+win+1):
					if j < 0 or j >= len(seq) or j == i:
						continue
					right.add(seq[j])
					fout.write(seq[i]+' '+seq[j]+' 1 1\n')

	# # Motif (Term)-Label
	# with open(file_path+dataset+'_data/labels_new.txt') as fin:
	# 	for line in fin:
	# 		data = line.strip()
	# 		motif = 'TERM_'+data
	# 		if len(motif2paper[motif]) < min_count:
	# 			print('Label name not frequent:', data)
	# 			exit()
	# 		label = 'LABEL_'+data
	# 		right.add(label)
	# 		fout.write(motif+' '+label+' 2 1\n')
				
with open(dataset+'/left.dat', 'w') as fou1, open(dataset+'/right.dat', 'w') as fou2:
	for x in left:
		fou1.write(x+'\n')
	for x in right:
		fou2.write(x+'\n')