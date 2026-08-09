# 04 — Pattern Recognition

## Overview

This stage asks a different question from the models in [`03_Deep_Learning_Response_Prediction/`](../03_Deep_Learning_Response_Prediction). Rather than predicting response from a sequence, it works backwards from measured response to identify **which compositional and positional features are associated with high glucose response** — and then uses those features to construct a new sequence library.

```
Screening results  →  Composition · position · k-mer analysis  →  Motif rules  →  Generated library
```

The analysis is deliberately interpretable. A neural network can rank a sequence without explaining it; the statistics here produce human-readable rules — *which nucleotide at which position*, *which k-mers*, *what GC content* — that guided sequence design and can be reported directly.

All analyses target the two chiralities that showed significant glucose response in screening: **(7,6)** and **(9,4)**.

---

## Methodology

The goal is to recognize patterns in the DNA library by analyzing nucleotide proportions, positions, and k-mer frequencies, identifying motifs relevant to the functional and structural properties of the sequences.

### Nucleotide proportions

For each sequence *S*, the proportion of each nucleotide *N* ∈ {A, C, G, T} characterizes its composition:

```
P(N) = count(N) / length(S)
```

where `count(N)` is the number of occurrences of *N* in *S*. Mean intensity per sequence is then computed and grouped by nucleotide proportion, giving the average signal intensity associated with different compositions.

### AT and GC content

Coarser compositional descriptors, obtained by summing the relevant proportions:

```
AT content = P(A) + P(T)
GC content = P(G) + P(C)
```

### Position analysis

This step resolves how the *position* of a nucleotide within a sequence influences response, rather than composition alone.

Given sequences `S = {DNA₁, DNA₂, …, DNAₙ}` with corresponding intensity responses `R = {R₁, R₂, …, Rₙ}`, each sequence's response is first **normalized by its length**:

```
r_ij = R_i / length(S_i)
```

where `r_ij` is the normalized response attributed to the *j*-th nucleotide of the *i*-th sequence. Length normalization matters here because the library spans multiple sequence lengths — without it, longer sequences would contribute disproportionately to positional averages.

Normalized responses are then aggregated across all sequences and averaged per nucleotide per position:

```
μ_jb = (1 / m_jb) · Σ r_ij   over all sequences carrying base b at position j
```

where `μ_jb` is the mean normalized response for nucleotide *b* at position *j*, and `m_jb` is the number of times *b* appears at position *j* across the library.

These values populate a matrix **M**, with `M_jb = μ_jb`, rendered as a heatmap (and as 3D surfaces of position × nucleotide × response) to expose positional hotspots — positions where a particular base is consistently associated with elevated response. Separate matrices are built for (7,6) and (9,4).

### K-mer analysis

Each sequence is decomposed into **overlapping** k-mers of length *k*. For *k* = 3, the sequence `AGCTGGTTC` yields `AGC`, `GCT`, `CTG`, and so on.

Frequency is the count of each k-mer across the whole library:

```
F(kmer) = count(kmer)
```

and the mean intensity response per k-mer is computed over all sequences containing it:

```
μ_kmer = mean(R) over sequences containing kmer
```

K-mers exhibiting **both high frequency and high response** are selected as the most effective in the dataset. This joint criterion is why the analysis plots frequency against mean response and applies elbow-method clustering — a high-response k-mer seen only once is not actionable evidence.

---

## Sequence generation

The positional matrices drive construction of a new library, implemented in `Position and prediction_Glucose.py`:

1. For each position, take the **top-two responding nucleotides** in `I₇₆` and in `I₉₄` independently
2. Where those sets **intersect**, sample from the common bases — favouring nucleotides that perform well for *both* chiralities
3. Where they don't intersect, fall back to the single best-responding base from each matrix and sample between them
4. Sequence length is drawn randomly between **8 and 14** nucleotides
5. Each generated sequence is scored by summing its positional responses across both matrices

The ranked library is exported to `sequences_with_High.xlsx`, passed to the trained ensemble in [`03_Deep_Learning_Response_Prediction/`](../03_Deep_Learning_Response_Prediction) for scoring, and the top predictions returned to [`02_HighThroughput_Screening_NIR_Pipeline/`](../02_HighThroughput_Screening_NIR_Pipeline) for experimental validation.

High-response k-mers identified above provide a second, independent generation route: they are recombined at high frequency to build sequences of varying length, retaining the properties observed in the high-response k-mers.

---

## Files

| Script | Purpose | Notes |
|---|---|---|
| `first_round_result_visulization.py` | First screening round — intensity and shift plots, sequence-length effect | Base version |
| `first_round_result_visulization 2.py` | First round, extended — per-chirality intensity and shift | Extended version of the above |
| `first_round_result_visulizationmutationround.py` | Mutation round — intensity, shift, box/scatter distributions | |
| `Proportion of each nucleotide_Glucose.py` | Per-base proportion vs. response | |
| `GC_AT_content_Glucose.py` | GC and AT content vs. response, per chirality | |
| `Position and prediction_Glucose.py` | **Position × nucleotide response matrices, heatmaps, and sequence generation** | Main script — produces the generated library |
| `K-mer analysis last version 2023.06_Glucose.py` | K-mer frequency vs. mean response, elbow method, clustering | |
| `3surface plot 2_Glucose.py` | 3D surface of position × nucleotide × response (matplotlib + plotly) | Base version |
| `3Dplot of propotion_Glucose.py` | 3D surfaces with integrated heatmaps, additional view angles and plotly export | Extended version of the above |

---

## Input data

Scripts expect the following files in the working directory:

| File | Used by |
|---|---|
| `133DNAfromDiffLeng-Final.xlsx` | Proportion, GC/AT, position, k-mer, and 3D surface scripts |
| `First Round.xlsx` (incl. sheet `lengths effect`) | First-round visualization scripts |
| `Mutation Round.xlsx` | Mutation-round visualization |

Expected columns in the main dataset: `DNA`, `(7,6) Intensity`, `(9,4) Intensity`, and the corresponding peak-shift columns. Several scripts address columns by integer index (`df.iloc[...]`) rather than by name, so column order must be preserved.

---

## Outputs

Figures are written to the working directory at 900 dpi: nucleotide proportion plots, GC/AT content plots, positional heatmaps for both chiralities, 3D response surfaces, k-mer frequency/response scatter and elbow plots, and per-round intensity and shift plots.

The generated sequence library is written to `sequences_with_High.xlsx`, with each sequence's summed positional response for both chiralities.

---

## Notes

- Generation draws from a set, so export order varies between runs; the sequences and their scores are unaffected.
- The generation loop is bounded by an attempt counter as well as a target count, so the number of unique sequences produced depends on how much the constrained per-position alphabet limits the reachable space.
- When a generated sequence exceeds the length of the positional matrix, position indices wrap by modulo, so positional preferences repeat cyclically.

---

## Reference

Rabbani, Y., Bregy, J., Rousseau, B., Sajjadi, S. H., De Benedittis, L., Behjati, S., Mouhib, M., Dehury, S., Boghossian, A. A. *"Discovery of a DNA-based Optical Nanotube Sensor for Glucose Using Clustering and Deep Learning Algorithms."* bioRxiv, 2025. [doi:10.1101/2025.05.06.652529](https://doi.org/10.1101/2025.05.06.652529)

Related to European Patent Application EP:24211885.9.
