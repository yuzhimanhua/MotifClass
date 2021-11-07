import json

dataset = 'MAG'
file_path = '../'

paper2idx = {}
with open(file_path+dataset+'_data/'+dataset+'_clean_new.json') as fin:
	for idx, line in enumerate(fin):
		js = json.loads(line)
		paper2idx[js['paper']] = str(idx)

topK = 50
with open(dataset+'_jointrep_'+str(topK)+'.txt') as fin, open(f'../MotifClass/{dataset.lower()}/doc_id.txt', 'w') as fout:
	for idx, line in enumerate(fin):
		fout.write(str(idx)+':')
		data = line.strip().split()[1:]
		papers = [paper2idx[x.split('_')[1]] for x in data]
		times = int((topK-1) / len(papers)) + 1
		papers = (papers*times)[:topK]
		fout.write(','.join(papers)+'\n')