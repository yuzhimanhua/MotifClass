import json
from collections import defaultdict

dataset = 'Amazon'
file_path = '../'

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

min_count = 5
with open(dataset+'_motif_matching.txt', 'w') as fout:
	for motif in motif2paper:
		if len(motif.split()) >= 2:
			print(motif)
		if len(motif2paper[motif]) >= min_count:
			fout.write(motif+'\t'+' '.join(motif2paper[motif])+'\n')
