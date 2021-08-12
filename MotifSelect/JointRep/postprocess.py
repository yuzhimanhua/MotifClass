import argparse

parser = argparse.ArgumentParser(description='main', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--dataset', default='MAG', choices=['MAG', 'Amazon'])

args = parser.parse_args()
dataset = args.dataset

cnt = 0
with open(dataset+'.emb') as fin:
	for idx, line in enumerate(fin):
		if idx == 0:
			continue
		data = line.strip().split()
		node = data[0]
		if ',' in node:
			continue
		cnt += 1

with open(dataset+'.emb') as fin, open(f'../../MotifClass/{dataset.lower()}/embedding_joint', 'w') as fout:
	fout.write(str(cnt)+' 100\n')
	for idx, line in enumerate(fin):
		if idx == 0:
			continue
		data = line.strip().split()
		node = data[0]
		if ',' in node:
			continue	
		if node.startswith('TERM_'):
			node = node[5:]
		fout.write(node+' '+' '.join(data[1:])+'\n')
