import json
from collections import defaultdict

dataset = 'MAG'
file_path = '../'

motif2paper = defaultdict(list)
with open(file_path+dataset+'_data/'+dataset+'_clean_new.json') as fin:
	for idx, line in enumerate(fin):
		if idx % 10000 == 0:
			print(idx)
		js = json.loads(line)
		P = 'PAPER_'+js['paper']
		
		# Venue
		V = js['venue']
		motif = 'VENUE_'+V
		motif2paper[motif].append(P)

		# Venue-Year
		Y = js['year']
		motif = 'VENUE_'+V+','+'YEAR_'+Y
		motif2paper[motif].append(P)

		# Venue-Author
		for A in js['author']:
			motif = 'VENUE_'+V+','+'AUTHOR_'+A
			motif2paper[motif].append(P)

		# Author
		for A in js['author']:
			motif = 'AUTHOR_'+A
			motif2paper[motif].append(P)

		# Author-Year
		for A in js['author']:
			motif = 'AUTHOR_'+A+','+'YEAR_'+Y
			motif2paper[motif].append(P)

		# Author-Author
		for A1 in js['author']:
			for A2 in js['author']:
				if A1 < A2:
					motif = 'AUTHOR_'+A1+','+'AUTHOR_'+A2
					motif2paper[motif].append(P)

		# Term
		for T in js['text'].split():
			motif = 'TERM_'+T
			motif2paper[motif].append(P)

min_count = 5
with open(dataset+'_motif_matching.txt', 'w') as fout:
	for motif in motif2paper:
		if len(motif.split()) >= 2:
			print(motif)
		if len(motif2paper[motif]) >= min_count:
			fout.write(motif+'\t'+' '.join(motif2paper[motif])+'\n')
