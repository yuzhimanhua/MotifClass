# MotifClass: Weakly Supervised Text Classification with Higher-order Metadata Information

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

This repository contains the source code for [**MotifClass: Weakly Supervised Text Classification with Higher-order Metadata Information**](https://arxiv.org/abs/2111.04022).

## Links

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Data](#data)
- [Running on New Datasets](#running-on-new-datasets)
- [Citation](#citation)


## Installation
For training, a GPU is strongly recommended.

### Keras
The code is based on Keras. You can find installation instructions [**here**](https://keras.io/#installation).

### Python Dependency
The code is written in Python 3.6. The dependencies are summarized in the file ```requirements.txt```. You can install them like this:
```
pip3 install -r requirements.txt
```

### GSL and Eigen Packages
The embedding code is written in C++ and depends on two packages: [**GSL**](https://www.gnu.org/software/gsl/) and [**Eigen**](http://eigen.tuxfamily.org/index.php?title=Main_Page). For Eigen, we already provide a zip file ```./motif_selection/eigen-3.3.3.zip```. You can directly unzip it in ```./motif_selection/```. For GSL, you can download it [here](https://drive.google.com/file/d/1UvmgrZbycC7wYAHahYGRB5pRtu6Aurhv/view?usp=sharing). After installing the two packages, you need to compile the embedding code:
```
cd motif_selection/
make
```

## Quick Start
To reproduce the results in our paper, you need to first download the [**datasets**](https://drive.google.com/file/d/1LQnHK9Cd6zSrQTASc4xauHLv2LFVFw_r/view?usp=sharing). Two datasets are used in our paper: **MAG-CS** and **Amazon**. Once you unzip the downloaded file (i.e., ```datasets.zip```), you can see two folders ```mag_data/``` and ```amazon_data/``` corresponding to these two datasets, respectively. You need to put these two folders under the main folder ```./```. Then the following scripts can be used to run the model.

```
./selection.sh
./classification.sh
```

Micro-F1, Macro-F1 and the confusion matrix will be shown in the last several lines of the output. The classification result can be found under ```./text_classification/{dataset}/```. For example, if you are using the MAG-CS dataset, the output will be ```./text_classification/mag/out.txt```.

## Data
Two datasets, **MAG-CS** and **Amazon**, are used in our paper. Dataset statistics are as follows:
| Dataset | #Documents | #Categories | Metadata Fields | 
| ------- | ---------- | ----------- | --------------- |
| MAG-CS | 203,157 | 20 | Author, Venue, Year |
| Amazon | 100,000 | 10 | User, Product |

After you download the [**datasets**](https://drive.google.com/file/d/1LQnHK9Cd6zSrQTASc4xauHLv2LFVFw_r/view?usp=sharing), there are three input files in each dataset folder: **```dataset.json```**, **```labels.txt```**, and **```motifs.txt```**.

```dataset.json``` has text and metadata information of each document. Each line is a json record representing one document. For example,
```
{
   "document":"3022911403",
   "author":[
      "3021171202", "2999350943", "3000115053", "2999233743"
   ],
   "venue":[
      "VLDB"
   ],
   "year":[
      "2009"
   ],
   "text":"modeling and querying possible repairs in duplicate_detection one of the most prominent data_quality problems is the existence of duplicate records current duplicate elimination procedures usually produce one clean instance repair of the input data by car",
   "label":"data_mining"
}
```
Here, "document" is the document id (it does not have specific meanings; just make sure different documents have different ids); "author", "venue", and "year" are metadata fields.

**NOTE: If you would like to run our code on your own dataset, when you prepare this json file, make sure: (1) The "document", "text", and "label" fields are provided. (2) For each document, its metadata field is always represented by a list of strings. For example, the "year" field should be \["2009"\] instead of 2009 or "2009". You can define your own metadata fields, not necessarily "author", "venue", or "year".** 

```labels.txt``` is the list of category names. For example,
```
information_retrieval
computer_hardware
programming_language
theoretical_computer_science
speech_recognition
real_time_computing
database
embedded_system
multimedia
machine_learning
natural_language_processing
software_engineering
computer_network
world_wide_web
computer_security
computer_graphics
parallel_computing
data_mining
human_computer_interaction
computer_vision
```
These names (either words or phrases) must appear in at least 5 documents in the dataset. Each label will have a label id according to its line number in ```labels.txt```. For example, "information_retrieval" has the label id 0; "computer_hardware" has the label id 1. After classification, the predicted label of each document will be represented by their label id in ```out.txt```.

```motifs.txt``` is the list of user-specified motif patterns. For example,
```
venue
author
venue,year
author,author
venue,author
author,year
term
```
All the metadata fields here, except "term", must be a metadata field in ```dataset.json```.

## Running on New Datasets
If you need to run our code on your own dataset, please follow the steps below.

(1) Create a directory named ```${dataset}_data``` under the main folder (e.g., ```./mag_data```).

(2) Prepare three files **```dataset.json```**, **```labels.txt```**, and **```motifs.txt```**. Please refer to the [Data](#data) section for more details.

(3) Run the script of selection and classification.
```
./selection.sh
./classification.sh
```

## Citation
If you find this repository useful, please cite the following paper:
```
@inproceedings{zhang2022motifclass,
  title={MotifClass: Weakly Supervised Text Classification with Higher-order Metadata Information},
  author={Zhang, Yu and Garg, Shweta and Meng, Yu and Chen, Xiusi and Han, Jiawei},
  booktitle={WSDM'22},
  pages={1357--1367},
  year={2022}
}
```
