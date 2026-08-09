# 04 — Pattern Recognition

## Overview

This stage asks a different question from the models in [`03_Deep_Learning_Response_Prediction/`](../03_Deep_Learning_Response_Prediction). Rather than predicting response from a sequence, it works backwards from measured response to identify **which compositional and positional features are associated with high glucose response** — and then uses those features to construct a new sequence library.

```
Screening results  →  Composition · position · k-mer analysis  →  Motif rules  →  Generated library
```

The analysis is deliberately interpretable. A neural network can rank a sequence without explaining it; the statistics here produce human-readable rules — *which nucleotide at which position*, *which k-mers*, *what GC content* — that guided sequence design and can be reported directly in the paper.

All analyses target the two chiralities that showed significant glucose response in screening: **(7,6)** and **(9,4)**.

---

## Analyses

**Screening-round visualization.** Intensity change and wavelength shift per sequence for the first screening round and the subsequent mutation round, including the effect of sequence length and box/scatter distributions across mutants.

**Nucleotide proportion analysis.** Proportion of each base (A, T, G, C) per sequence plotted against measured response, testing whether overall base composition alone carries signal.

**GC / AT content.** GC and AT content against response for each chirality — a coarser compositional descriptor than per-base proportion, and one directly tied to duplex stability and stacking behaviour.

**Position analysis.** The core method. For every position *j* and nucleotide *b*, the mean response across all sequences carrying *b* at *j* is computed, producing intensity-response matrices `I₇₆(j,b)` and `I₉₄(j,b)`. These are rendered as heatmaps and as 3D surfaces (position × nucleotide × mean response), revealing positions where a specific base is consistently associated with elevated response.

**K-mer analysis.** K-mer frequency across the library related to mean response, with elbow-method selection and clustering to separate high-response from low-response k-mer groups.

---

## Sequence generation

The positional matrices are used directly to construct a new library, implemented in `Position and prediction_Glucose.py`:

1. For each position, take the **top-two responding nucleotides** in `I₇₆` and in `I₉₄` independently
2. Where those two sets **intersect**, sample from the common bases — favouring nucleotides that perform well for *both* chiralities
3. Where they don't intersect, fall back to the single best-responding base from each matrix and sample between them
4. Sequence length is drawn randomly between **8 and 14** nucleotides
5. Each generated sequence is scored by summing its positional responses across both matrices

The result is exported as a ranked candidate library (`sequences_with_High.xlsx`), which is then passed to the trained ensemble in [`03_Deep_Learning_Response_Prediction/`](../03_Deep_Learning_Response_Prediction) for scoring, and the top predictions returned to [`02_HighThroughput_Screening_NIR_Pipeline/`](../02_HighThroughput_Screening_NIR_Pipeline) for experimental validation.

High-response k-mers identified in the k-mer analysis are likewise recombined at high frequency to build sequences of varying length, providing a second, independent generation route.

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

Expected columns in the main dataset: DNA sequence, `(7,6) Intensity`, `(9,4) Intensity`, and the corresponding peak-shift columns. Note that several scripts address columns by integer index (`df.iloc[...]`) rather than by name, so column order must be preserved.

---

## Outputs

Figures are written to the working directory at 900 dpi: nucleotide proportion plots, GC/AT content plots, positional heatmaps for both chiralities, 3D response surfaces, k-mer frequency/response scatter and elbow plots, and per-round intensity and shift plots.

The generated sequence library is written to `sequences_with_High.xlsx` with each sequence's summed positional response for both chiralities.

---

## Notes

- Generation draws from a set, so the export order varies between runs; the sequences and their scores are unaffected.
- The generation loop is bounded by an attempt counter as well as a target count, so the number of unique sequences produced depends on how much the constrained alphabet at each position limits the reachable space.
- `Position and prediction_Glucose.py` wraps position indices with a modulo when a generated sequence is longer than the positional matrix, so positional preferences repeat cyclically beyond the matrix length.

---

## Reference

Rabbani, Y., Bregy, J., Rousseau, B., Sajjadi, S. H., De Benedittis, L., Behjati, S., Mouhib, M., Dehury, S., Boghossian, A. A. *"Discovery of a DNA-based Optical Nanotube Sensor for Glucose Using Clustering and Deep Learning Algorithms."* bioRxiv, 2025. [doi:10.1101/2025.05.06.652529](https://doi.org/10.1101/2025.05.06.652529)

Related to European Patent Application EP:24211885.9.
