# Embryo and Sperm Classification Models Using Transfer Learning

This project aims to develop models that aid in the IVF process by classifying embryo and sperm images as good or bad. The models use transfer learning with ResNet101 and VGG16 to achieve high accuracies.


## Link to the datasets: https://osf.io/3kc2d/


## Project Overview
The goal of this project is to improve the efficiency, precision, and success rates of IVF procedures by automating the classification of embryo and sperm images. The embryo model classifies images as either blastocysts (good) or non-blastocysts (bad). The sperm model classifies images as good or bad depending on the presence if blastocysts.


## Dependencies
The project requires the following libraries:

- pandas
- scikit-learn
- pillow
- matplotlib
- torch
- torchvision


## Modeling
### Model Selection
The ResNet101 model was chosen for the embryo images and the VGG16 model was choosen for the sperm images. This was due to their proven performance in similar classification tasks. The modesl were fine-tuned using the preprocessed and augmented dataset.

### Training, Testing, and Evaluation
- Training: The models were trained using the processed datasets, achieving a high accuracy.
- Testing: The models' performance was evaluated on a test set, resulting in a test accuracy of 93% for the embryo model, and an accuracy of 99% for the sperm model.


## Usage
To run this project, follow these steps:

- Install the required dependencies.
- Load the datasets from the specified path.
- Execute the provided notebooks to preprocess the data, perform data augmentation, train the model, and evaluate its performance.

## Demo

https://github.com/sottohy/VEE-ML/assets/91037437/afb6bfd7-23c3-483a-a615-cf999ddfed9d


