# The code structure is adapted from the WeSTClass implementation
# https://github.com/yumeng5/WeSTClass

import os
os.environ["CUDA_DEVICE_ORDER"]="PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

import numpy as np
np.random.seed(1234)
from time import time
from model import WSTC, f1
from keras.optimizers import SGD
from gen import augment, pseudodocs
from load_data import load_dataset
from gensim.models import word2vec
from gensim.models import KeyedVectors
from sklearn import preprocessing


def load_embedding(vocabulary_inv, num_class, dataset_name, embedding_name):
	model_name = f'{dataset_name}/embedding_{embedding_name}'
	if os.path.exists(model_name):
		# embedding_model = word2vec.Word2Vec.load(model_name)
		embedding_model = KeyedVectors.load_word2vec_format(model_name, binary = False, unicode_errors='ignore')
		print("Loading existing embedding vectors {}...".format(model_name))
	else:
		print("Cannot find the embedding file!")

	embedding_weights = {key: embedding_model[word] if word in embedding_model else
						np.random.uniform(-0.25, 0.25, embedding_model.vector_size)
						 for key, word in vocabulary_inv.items()}

	label_name = f'../{dataset_name}_data/labels.txt'
	if os.path.exists(label_name):
		centers = [None for _ in range(num_class)]
		with open(label_name) as fin:
			for idx, line in enumerate(fin):
				label = line.strip()
				centers[idx] = embedding_model[label] / np.linalg.norm(embedding_model[label])

	return embedding_weights, centers


def write_output(write_path, y_pred, perm):
	invperm = np.zeros(len(perm), dtype='int32')
	for i,v in enumerate(perm):
		invperm[v] = i
	y_pred = y_pred[invperm]
	with open(os.path.join(write_path, 'out.txt'), 'w') as f:
		for val in y_pred:
			f.write(str(val) + '\n')
	print("Classification results are written in {}".format(os.path.join(write_path, 'out.txt')))
	return


if __name__ == "__main__":

	import argparse

	parser = argparse.ArgumentParser(description='main',
									 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	
	### Basic settings ###
	# dataset selection: MAG-CS (default), Amazon
	parser.add_argument('--dataset', default='mag', choices=['mag', 'amazon'])
	# embedding files: joint embedding (default)
	parser.add_argument('--embedding', default='joint')
	# whether ground truth labels are available for evaluation: True (default), False
	parser.add_argument('--with_evaluation', default='True', choices=['True', 'False'])
	
	### Training settings ###
	# mini-batch size for both pre-training and self-training: 256 (default)
	parser.add_argument('--batch_size', default=256, type=int)
	# training epochs: dataset-specific
	parser.add_argument('--pretrain_epochs', default=None, type=int)

	### Hyperparameters settings ###
	# number of generated pseudo documents per class: dataset-specific
	parser.add_argument('--num_generated_docs', default=None, type=int)
	# keyword vocabulary size (gamma): 50 (default)
	parser.add_argument('--gamma', default=50, type=int)
	# vmf concentration parameter when synthesizing documents (kappa): dataset-specific
	parser.add_argument('--kappa', default=None, type=float)
	# number of copies each retrieved/generated pseudo-labeled document has in one epoch
	parser.add_argument('--ratio', default=10, type=int)
	
	### Dummy arguments (please ignore) ###
	# weak supervision selection: labeled documents (default)
	parser.add_argument('--sup_source', default='docs', choices=['docs'])
	# maximum self-training iterations: 0 (default)
	parser.add_argument('--maxiter', default=0, type=int)
	# self-training update interval: None (default)
	parser.add_argument('--update_interval', default=None, type=int)
	# background word distribution weight (alpha): 0.0 (default)
	parser.add_argument('--alpha', default=0.0, type=float)
	# self-training stopping criterion (delta): None (default)
	parser.add_argument('--delta', default=0.1, type=float)
	# trained model directory: None (default)
	parser.add_argument('--trained_weights', default=None)

	args = parser.parse_args()
	print(args)

	alpha = args.alpha
	gamma = args.gamma
	delta = args.delta
	ratio = args.ratio

	word_embedding_dim = 100

	update_interval = 50
	self_lr = 1e-3

	if args.dataset == 'mag':
		pretrain_epochs = 100
		max_sequence_length = 200
		num_generated_docs = 50
		kappa = 200
		beta = num_generated_docs * ratio
		
	elif args.dataset == 'amazon':
		pretrain_epochs = 100
		max_sequence_length = 200
		num_generated_docs = 100
		kappa = 150
		beta = num_generated_docs * ratio

	decay = 1e-6
	
	if args.update_interval is not None:
		update_interval = args.update_interval
	if args.pretrain_epochs is not None:
		pretrain_epochs = args.pretrain_epochs

	if args.with_evaluation == 'True':
		with_evaluation = True
	else:
		with_evaluation = False

	if args.sup_source == 'docs':
		x, y, word_counts, vocabulary, vocabulary_inv_list, len_avg, len_std, word_sup_list, sup_idx, perm = \
			load_dataset(args.dataset, model='cnn', sup_source=args.sup_source, with_evaluation=with_evaluation, truncate_len=max_sequence_length)
	
	np.random.seed(1234)
	vocabulary_inv = {key: value for key, value in enumerate(vocabulary_inv_list)}
	vocab_sz = len(vocabulary_inv)
	n_classes = len(word_sup_list)    

	if x.shape[1] < max_sequence_length:
		max_sequence_length = x.shape[1]
	x = x[:, :max_sequence_length]
	sequence_length = max_sequence_length

	print("\n### Input preparation ###")
	embedding_weights, centers = load_embedding(vocabulary_inv, n_classes, args.dataset, args.embedding)
	embedding_mat = np.array([np.array(embedding_weights[word]) for word in vocabulary_inv])
	
	wstc = WSTC(input_shape=x.shape, n_classes=n_classes, y=y, model='cnn',
				vocab_sz=vocab_sz, embedding_matrix=embedding_mat, word_embedding_dim=word_embedding_dim)

	if args.trained_weights is None:
		print("\n### Phase 1: vMF distribution fitting & pseudo document generation ###")
		
		word_sup_array = np.array([np.array([vocabulary[word] for word in word_class_list]) for word_class_list in word_sup_list])
		
		total_counts = sum(word_counts[ele] for ele in word_counts)
		total_counts -= word_counts[vocabulary_inv_list[0]]
		background_array = np.zeros(vocab_sz)
		for i in range(1,vocab_sz):
			background_array[i] = word_counts[vocabulary_inv[i]]/total_counts
		seed_docs, seed_label = pseudodocs(word_sup_array, gamma, background_array,
										   sequence_length, len_avg, len_std, beta, alpha, 
										   vocabulary_inv, embedding_mat, centers, kappa, 'cnn', 
										   './results/{}/{}/phase1/'.format(args.dataset, 'cnn'))
		
		if args.sup_source == 'docs':
			num_real_doc = len(sup_idx.flatten()) * ratio
			real_seed_docs, real_seed_label = augment(x, sup_idx, num_real_doc)
			seed_docs = np.concatenate((seed_docs, real_seed_docs), axis=0)
			seed_label = np.concatenate((seed_label, real_seed_label), axis=0)

		perm_seed = np.random.permutation(len(seed_label))
		seed_docs = seed_docs[perm_seed]
		seed_label = seed_label[perm_seed]

		print('\n### Phase 2: pre-training with pseudo documents ###')

		wstc.pretrain(x=seed_docs, pretrain_labels=seed_label,
					 sup_idx=sup_idx, optimizer=SGD(lr=0.1, momentum=0.9),
					 epochs=pretrain_epochs, batch_size=args.batch_size,
					 save_dir='./results/{}/{}/phase2'.format(args.dataset, 'cnn'))

		y_pred = wstc.predict(x)
		if y is not None:
			f1_macro, f1_micro = np.round(f1(y, y_pred), 5)
			print('F1 score after pre-training: f1_macro = {}, f1_micro = {}'.format(f1_macro, f1_micro))

	else:
		print("\n### Directly loading trained weights ###")
		wstc.load_weights(args.trained_weights)
		y_pred = wstc.predict(x)
		if y is not None:
			f1_macro, f1_micro = np.round(f1(y, y_pred), 5)
			print('F1 score: f1_macro = {}, f1_micro = {}'.format(f1_macro, f1_micro))
	
	print("\n### Generating outputs ###")
	write_output('./' + args.dataset, y_pred, perm)
