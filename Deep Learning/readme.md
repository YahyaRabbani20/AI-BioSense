# 03 — Deep Learning: Sequence-to-Response Prediction

## Overview

This stage learns the mapping from **DNA sequence → glucose response** using the chirality-resolved labels produced in [`02_HighThroughput_Screening_NIR_Pipeline/`](../02_HighThroughput_Screening_NIR_Pipeline), then applies the trained model to score a large generated sequence library and nominate candidates for experimental validation.

```
Labelled screen  →  Encode  →  Train CNN / GNN / GCN  →  Majority vote  →  Score ~100k sequences  →  Validate
```

Three architectures are trained **in parallel rather than in competition**. Each consumes a different representation of the same sequence — a positional matrix (CNN) and two k-mer graph formulations (GNN, GCN) — so that complementary information is captured: the CNN sees position and local motif structure, the graph models see k-mer composition and connectivity. Predictions are combined by majority voting at inference.

---

## Prediction target

The models perform **binary classification** of PL intensity change in response to glucose, using the two chiralities that showed significant response in screening: **(7,6)** and **(9,4)**.

| Property | Value |
|---|---|
| Input | ssDNA sequence |
| Output | High vs. low PL intensity response |
| Binarization threshold | PL intensity change of **12** |
| Response channels | (7,6) and (9,4) |
| Class balance | Dataset balanced across high/low classes |

Binarizing rather than regressing is a deliberate choice: with a modest number of labelled sequences and non-trivial replicate variance, a two-class decision is far better conditioned than predicting a continuous response value.

---

## Data preprocessing

Labels originate from the deconvoluted spectra: intensity changes and peak shifts computed per chirality against paired PBS blanks. Among all measured chiralities, (7,6) and (9,4) showed the significant glucose-induced intensity changes and were therefore selected as the model output variables.

Sequences are then encoded by one of two routes, run in parallel to preserve complementary information:

- **Matrix encoding** — one-hot ("5-eye") representation for the CNN
- **Graph encoding** — k-mer graph representation for the GNN and GCN

---

## CNN model

**Encoding.** Each sequence is one-hot encoded into a matrix of size `fixed_length × 5`, where the five channels correspond to A, G, C, T, and N. Nucleotides are mapped to indices and expanded via a 5×5 identity matrix, then reshaped into a 4D tensor suitable for convolutional input.

**Architecture.** Convolutional layers → pooling layers → flattening → dense layers → binary output.

**Training.**
- Loss: binary cross-entropy
- Optimizer: selected among Adam, SGD, RMSprop during tuning
- Early stopping monitored on validation loss
- k-fold cross-validation

The convolutional layers act as learned motif detectors — the positional analogue of the k-mer features used elsewhere in the pipeline, but with the motif patterns learned from response data rather than enumerated in advance.

---

## GNN model

**Encoding.** Each sequence is converted into a **directed k-mer graph**: for a sequence `S = {s₁, s₂, …, sₙ}` and k-mer size *k*, nodes `V` are the unique k-mers and edges `E` connect overlapping consecutive k-mers. The graph `G = (V, E)` is then embedded into a fixed-dimensional vector `v ∈ ℝᵈ` using **Graph2Vec**.

**Architecture.** A feed-forward network over the Graph2Vec embedding:

- Input layer `x ∈ ℝᵈ`
- Hidden layers with weight matrices `Wᵢ`, biases `bᵢ`, and nonlinearity σ
- Output layer producing class probabilities

**Training.** Backpropagation minimizing cross-entropy loss, with the same Optuna hyperparameter search and k-fold cross-validation protocol as the CNN.

Graph2Vec produces a whole-graph embedding, so this model reasons about the sequence's k-mer composition and connectivity as a единое whole rather than position by position.

---

## GCN model

**Encoding.** Same directed k-mer graph construction as the GNN, but the graph is consumed directly rather than pre-embedded. Overlapping k-mers form nodes; the **adjacency matrix `A`** encodes connectivity and the **feature matrix `X`** is built by one-hot encoding each k-mer.

**Architecture.** Graph convolutional layers → dense classification layer.

**Training.**
- Optimizer: Adam
- Loss: binary cross-entropy
- Mini-batch training over graph data
- Optuna tuning and k-fold cross-validation as above

Where the GNN compresses the graph into a vector before learning, the GCN performs message passing on the graph itself — so it retains node-level structure that Graph2Vec discards.

---

## Hyperparameter optimization

All hyperparameters across the three architectures are optimized with **Optuna**, with the objective defined to minimize loss across k-fold cross-validation. Tuned parameters include:

- Number of convolutional filters and kernel sizes
- Dense layer units
- Dropout rates
- Learning rates
- Pooling type
- Optimizer choice
- Number of folds *k*

k-fold cross-validation divides the dataset into *k* equal folds; the model trains on *k*−1 folds and tests on the held-out fold, rotating until each fold has served as test set once, with results averaged into a single performance metric. This guards against both overfitting and underfitting given the dataset size.

Best hyperparameters are persisted for reuse at inference.

---

## Evaluation

Models are assessed via the **confusion matrix** (TP, TN, FP, FN) and derived metrics:

| Metric | Definition |
|---|---|
| True Positive Rate (TPR) | TP / (TP + FN) |
| True Negative Rate (TNR) | TN / (TN + FP) |
| Accuracy | (TP + TN) / (TP + FP + TN + FN) |

Additionally reported: precision, recall, F1 score, and **ROC AUC**. The ROC curve plots true positive rate against false positive rate; AUC represents the probability that a randomly chosen positive case is ranked above a randomly chosen negative one, and collapses classifier performance into a single comparable number across the three architectures.

---

## Prediction and candidate screening

**Ensemble.** At inference, the three trained models are combined by **majority voting**, so a candidate is nominated only where independent representations of the sequence agree.

**Library scoring.** Approximately **100,000 new DNA sequences** were generated and scored with the optimized ensemble. Sequences with high predicted probability of a high-intensity response were selected for experimental validation.

The generated library is not random — it is constructed from motifs identified in pattern recognition analysis:

- **Position-informed generation** — nucleotides chosen from the positional intensity-response matrices for (7,6) and (9,4), favouring bases with top response at each position and, where possible, bases scoring highly in *both* chirality datasets
- **K-mer-informed generation** — high-response k-mers recombined at varying frequencies to build sequences of different lengths

Selected candidates return to [`02_HighThroughput_Screening_NIR_Pipeline/`](../02_HighThroughput_Screening_NIR_Pipeline) for experimental validation, closing the design–test–learn loop.

---

## Repository contents

| Folder | Contents |
|---|---|
| [`Data_Preprocessing/`](./Data_Preprocessing) | Label binarization at the intensity threshold, class balancing, one-hot and k-mer graph encoding |
| [`CNN/`](./CNN) | One-hot (5-eye) encoding, convolutional architecture, training loop |
| [`GNN/`](./GNN) | k-mer graph construction, Graph2Vec embedding, dense classifier |
| [`GCN/`](./GCN) | k-mer adjacency and feature matrices, graph convolutional architecture |
| [`Hyperparameter_Optimization/`](./Hyperparameter_Optimization) | Optuna studies, search spaces, k-fold configuration, best-parameter records |
| [`Evaluation/`](./Evaluation) | Confusion matrix, ROC/AUC, precision/recall/F1 reporting |
| [`Prediction_and_Screening/`](./Prediction_and_Screening) | Majority-vote ensemble, scoring of the ~100k generated library, candidate ranking |

---

## Reference

Rabbani, Y., Bregy, J., Rousseau, B., Sajjadi, S. H., De Benedittis, L., Behjati, S., Mouhib, M., Dehury, S., Boghossian, A. A. *"Discovery of a DNA-based Optical Nanotube Sensor for Glucose Using Clustering and Deep Learning Algorithms."* bioRxiv, 2025. [doi:10.1101/2025.05.06.652529](https://doi.org/10.1101/2025.05.06.652529)

Related to European Patent Application EP:24211885.9.
