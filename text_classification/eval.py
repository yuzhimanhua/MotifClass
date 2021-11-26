from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
import argparse

parser = argparse.ArgumentParser(description='main', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--dataset', default='mag', choices=['mag', 'amazon'])

args = parser.parse_args()
dataset = args.dataset

y = []
with open(f'{dataset}/dataset.csv') as fin:
	for line in fin:
		y.append(line.strip().split(',')[0])

y_pred = []
with open(f'{dataset}/out.txt') as fin:
	for line in fin:
		y_pred.append(line.strip())

print(f1_score(y, y_pred, average='micro'))
print(f1_score(y, y_pred, average='macro'))

print(confusion_matrix(y, y_pred))