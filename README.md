# MotifClass: Weakly Supervised Text Classification with Higher-order Metadata Information

## Installation
For training, a GPU is strongly recommended.

### Keras
The code is based on Keras. You can find installation instructions [**here**](https://keras.io/#installation).

### Dependency
The dependencies are summarized in the file ```requirements.txt```. You can install them like this:

```
pip3 install -r requirements.txt
```

## Quick Start
To reproduce the results in our paper, you need to first download the [**datasets**](https://gofile.io/d/Ra5EH7). Two datasets are used in our paper: **MAG-CS** and **Amazon**. Once you unzip the downloaded file (i.e., ```MotifClass_QuickStart.zip```), you can see two folders. Put them under ```./MotifClass/```. Then the following running script can be used to run the model.

```
cd MotifClass/
./test.sh
```

Micro-F1/Macro-F1 scores will be shown in the last several lines of the output. The classification result can be found under your dataset folder. For example, if you are using the MAG-CS dataset, the output will be ```./MotifClass/mag/out.txt```.

## Datasets
The JSON version of the two datasets can be downloaded [**here**](https://gofile.io/d/JXPZyt).

## Running MotifClass from Scratch
After downloading the JSON version of the two datasets, unzip it (i.e., ```MotifClass_Datasets.zip```), and put the unziped folders under the main folder ```./```.

Then, you need to first run joint representation learning, motif instance selection, and pseudo training data retrieval. To do this,

```
cd MotifSelect/
./run.sh
```

After that, go back to the ```./MotifClass``` folder and run the classification code.

```
cd ../MotifClass/
./test.sh
```
