# 01 — Discovery & Sequence Design: ML Clustering for Diverse ssDNA Selection

## Overview

Before any wet-lab screening, the candidate ssDNA sequence space is reduced from thousands of possibilities down to a small, information-rich set using three independent clustering strategies — **similarity-based (MAFFT)**, **pattern-based (k-mers)**, and **structure-based (RNA folding)**. Each strategy defines its own "sequence space," and K-means clustering (with the elbow method to pick *k*) selects one representative sequence per cluster for experimental screening. This step corresponds to stage **A** in the overall discovery pipeline.

The core assumption: sequences that cluster together by sequence similarity, motif content, or predicted secondary structure tend to share intrinsic properties (base composition, loop geometry, flexibility) that bias how they adsorb onto and interact with a carbon nanotube surface — so testing one representative per cluster is sufficient to sample a behavioral class, rather than testing every candidate individually.

---

## Method 1: Similarity-based clustering (MAFFT)

Sequences are pairwise-aligned with the **MAFFT** algorithm, and a similarity index is computed from the aligned positions.

For a sequence set `S = {s1, s2, ..., sn}`, the alignment is `A = MAFFT(S)`.

For two aligned sequences `si`, `sj`, the pairwise similarity index is:

```
sim_ij = (1/L) * Σ_{k=1..L} δ(a_ik, a_jk)
```

where `L` is the alignment length, and `δ(x,y) = 1` if the nucleotides match, `0` otherwise.

Each sequence's overall similarity score is the average of its pairwise similarity indices against all others:

```
Similarity_index(s_i) = Average(sim_i,1, sim_i,2, ..., sim_i,n)
```

These per-sequence similarity indices form the feature space that K-means clusters over.

---

## Method 2: Pattern-based clustering (k-mers)

Each sequence is decomposed into overlapping **k-mers** (e.g. k = 5 over a 30-nucleotide sequence), and nucleotide composition within those motifs is used to build a feature vector.

**Motif encoding:**

```
M(S_i) = (1/k) * Σ_{j=1..k} [count(A), count(C), count(G), count(T)]_j
```

Each sequence `S_i` is split into motifs of length `k`, and nucleotide counts within each motif form the feature vector used for clustering (visualized as a DNA-sequence × k-mer-frequency heatmap). A one-hot nucleotide encoding (e.g. `AGCT` → 4×4 identity-style matrix) is used as a complementary sequence representation.

---

## Method 3: DNA/RNA folding-based clustering (ViennaRNA)

Secondary structure is predicted per sequence with **ViennaRNA**, classifying each into fold types (hairpin-loop, internal loop, circular, stem-loop, etc.) and computing thermodynamic descriptors:

**Minimum free energy (MFE):**
```
ΔG(S) = Σ ΔG(structural elements)
```
Total Gibbs free energy of secondary structure `S`, summed over base pairs, loops, and unpaired regions.

**Partition function:**
```
Z = Σ_{s∈S} e^(−ΔG(s)/RT)
```

**Ensemble free energy:**
```
G = −RT · ln(Z)
```

**Base-pairing probability** (probability that nucleotides `i` and `j` are paired):
```
P(i,j) = e^(−ΔG_pair(i,j)/RT) / Z
```

**Centroid structure** (the most representative fold in an ensemble — minimizes expected base-pair distance to all other structures, weighted by probability):
```
S_centroid = argmin_{s∈S} Σ_{s'∈S} d(s,s') · P(s')
```

Sequences are clustered on **free energy vs. paired probability**, colored by fold class.

### Additional DNA sequence descriptors (used alongside folding features)

- **Average atomic number / EIIP / molecular weight** per sequence: `avg_x = Σ x[nucleotide] / L`
- **Melting temperature:** `Tm = 64.9 + 41 × ((GC_content − 16.4) / L)`
- **Shannon entropy** of base composition: `entropy = −Σ_{b∈{A,C,G,T}} p_b · log2(p_b)`

### Why folding-based clustering is a valid proxy for ssDNA-SWCNT behavior

- **Shared intrinsic properties:** sequences with similar predicted folds share base composition, loop sizes, and flexibility — features known to bias adsorption mode on carbon nanotubes.
- **Behavioral grouping:** even where folds rearrange upon nanotube adsorption, sequences within the same folding cluster tend to show similar adsorption "phenotypes."
- **Efficient diversity sampling:** one representative per folding cluster is enough to cover distinct classes of ssDNA-SWCNT interaction, avoiding redundant screening.
- **Coarse-grained phenotype:** CNT surface behavior depends on broad traits (unpaired-base runs, rigidity, purine content) rather than exact fold geometry — which folding clusters capture.
- **Experimentally validated:** testing multiple sequences within the same cluster confirms that cluster membership predicts similar CNT response.

---

## Clustering: K-means + Elbow Method

Each feature space (MAFFT similarity, k-mer motifs, folding descriptors) is clustered independently with **K-means**, minimizing the within-cluster sum of squares:

```
WCSS(k) = Σ_{i=1..k} Σ_{x∈C_i} ||x − μ_i||²
```

where `C_i` is the set of points in cluster `i` and `μ_i` is its centroid.

The number of clusters `k` is chosen with the **elbow method**: WCSS is plotted against `k`, and the value where marginal reduction in WCSS sharply flattens ("the elbow") is selected — balancing cluster granularity against redundant sampling.

---

## Repository Contents

| Folder | Method | Contents |
|---|---|---|
| [`MAFFT_Similarity_Clustering/`](./MAFFT_Similarity_Clustering) | Similarity-based (Method 1) | MAFFT alignment and pairwise similarity index computation |
| [`Kmer_Pattern_Clustering/`](./Kmer_Pattern_Clustering) | Pattern-based (Method 2) | K-mer decomposition, motif encoding, one-hot sequence encoding |
| [`RNA_Folding_Clustering/`](./RNA_Folding_Clustering) | Folding-based (Method 3) | ViennaRNA folding, MFE / partition function / base-pairing probability, DNA descriptors (EIIP, Tm, entropy) |

Each folder's K-means clustering (with elbow-method selection of *k*) is run on that method's respective feature space independently, and representative sequences from each are pooled for experimental screening.

## Outputs

- Cluster assignments per sequence, per method (MAFFT / k-mer / folding)
- One representative sequence selected per cluster → passed to experimental HTS screening ([`02_Experimental_Preparation_Screening/`](../02_Experimental_Preparation_Screening))
- Cluster visualizations: similarity-index scatter plots, k-mer frequency heatmaps, and free-energy vs. paired-probability plots colored by fold class

## Reference

This method is described in: Rabbani, Y. et al., *"Discovery of a DNA-based Optical Nanotube Sensor for Glucose Using Clustering and Deep Learning Algorithms,"* bioRxiv, 2025. Related to European Patent Application EP:24211885.9.
