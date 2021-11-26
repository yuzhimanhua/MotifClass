# MotifClass: Weakly Supervised Text Classification with Higher-order Metadata Information

This paper provides a weakly supervised framework for metadata-aware document categorization, where no human-annotated training samples are needed.

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
To reproduce the results in our paper, you need to first download the [**datasets**](https://drive.google.com/file/d/1LQnHK9Cd6zSrQTASc4xauHLv2LFVFw_r/view?usp=sharing). Two datasets are used in our paper: **MAG-CS** and **Amazon**. Once you unzip the downloaded file (i.e., ```datasets.zip```), you can see two folders ```mag_data/``` and ```amazon_data``` corresponding to these two datasets, respectively. You need to put these two folders under the main folder ```./```. Then the following scripts can be used to run the model.

```
./selection.sh
./classification.sh
```

Micro-F1, Macro-F1 and the confusion matrix will be shown in the last several lines of the output. The classification result can be found under ```./text_classification/{dataset}/```. For example, if you are using the MAG-CS dataset, the output will be ```./text_classification/mag/out.txt```.

## Dataset
