# 02 — High-Throughput Screening and NIR Response Pipeline

## Overview

This stage closes the experimental half of the design–test–learn loop. Candidate ssDNA sequences proposed in [`01_Discovery_Sequence_Design/`](../01_Discovery_Sequence_Design) enter here as oligonucleotides and leave as **chirality-resolved, ML-ready response labels**.

```
Prepare  →  384-well screen  →  Acquire NIR fluorescence  →  Deconvolve spectra  →  Response
```

The pipeline is built as one integrated workflow: preparation, automated acquisition, and spectral processing share a single data structure, so every spectrum stays traceable to its sequence, analyte, replicate, and plate position. That traceability is what makes the dataset reusable across analytes rather than campaign-specific.

---

## Stage 1 — ssDNA-SWCNT preparation

Sensor constructs are produced by **surfactant exchange**, replacing the sodium cholate (SC) used to suspend the nanotubes with the target ssDNA sequence. The protocol is designed for low-volume, high-throughput preparation, which is what makes screening large sequence libraries affordable.

**Starting materials**

| Component | Specification |
|---|---|
| SWCNTs | Super-purified HiPco, mixed chirality (NanoIntegris) |
| ssDNA oligomers | Microsynth |
| SC-SWCNT stock | 30 mg SWCNT in 30 mL 2% sodium cholate (DI water) |

**SC-SWCNT suspension**
- Homogenized 20 min at 5,000 rpm
- Probe-tip ultrasonication, 1 h at 10% amplitude in an ice bath
- Centrifuged 30,000 rpm, 4 h, 25 °C; supernatant collected
- Normalized to **110 mg/L** by absorbance at 632 nm (UV-3600 Plus, Shimadzu)

**ssDNA stock**
- Dissolved in DI water, normalized to **50 µM** by absorbance at 260 nm (NanoDrop 2000, extinction coefficients via OligoCalc)
- Stored at −20 °C until use

**Exchange and purification**
- 60 µL ssDNA + 60 µL SC-SWCNT in 2 mL PCR-grade Eppendorf tubes
- 180 µL methanol added to raise the critical micelle concentration — SC desorbs from the nanotube surface into micelles, allowing ssDNA to wrap
- Centrifugation (1 h, 21 °C, 15,000 rpm), supernatant removed, 15 min rest to let ethanol traces evaporate without over-drying the pellet
- Resuspended in 300 µL DI water; 10X PBS added after 10 min to bring the sample to 1X PBS
- Homogenized > 1 h, then centrifuged (20 min, 21 °C, 15,000 rpm) and supernatant collected to remove aggregates
- **Normalized to 5 mg/L** by absorbance at 632 nm on a 50 µL aliquot in a 384-well plate (Varioscan LUX, Thermo Scientific)
- Stored overnight at RT in the dark before measurement

Concentration normalization is not a formality: because the readout is a *relative* intensity change, inconsistent starting concentration propagates directly into apparent response and inflates replicate variance.

---

## Stage 2 — High-throughput screening

Prepared constructs are arrayed in **384-well plate** format, screening many DNA sequences against the analyte in parallel.

| Parameter | Value |
|---|---|
| Plate format | 384-well |
| Sensor volume per well | 49 µL ssDNA-SWCNT at 5 mg/L |
| Addition | 1 µL analyte **or** 1X PBS blank |
| Analyte (glucose) final concentration | 7.5 mM in 1X PBS |
| Replication | Triplicate per DNA × condition |
| Addition interval | 45 s between wells |
| Incubation before measurement | 2 hours |
| Temperature | Room temperature |

Every sequence is measured **both with analyte and against a paired 1X PBS blank**, so response is always computed as a paired difference rather than an absolute intensity.

The 7.5 mM glucose concentration was selected to represent the physiological blood concentration in diabetic patients. The staggered 45 s addition interval mirrors the microscope's own traversal timing, so that **every well is read at the same elapsed time after addition** — 2 hours — rather than at the same wall-clock time. Without this, incubation time would vary systematically across the plate and be confounded with well position.

---

## Stage 3 — NIR fluorescence acquisition

Photoluminescence is measured on a custom-built near-infrared microscope under automated control.

| Component | Specification |
|---|---|
| Excitation source | Supercontinuum laser with tunable band-pass and short-pass filters |
| Excitation wavelengths | **655 nm** and **735 nm** (10 nm bandwidth) |
| Objective | 20X, with dichroic beam splitter |
| Exposure | 10 s at maximum relative power |
| Detection | InGaAs NIR detector |
| Emission range | 900–1400 nm |
| Acquisition control | LightField software, coordinated by a LabVIEW program |

The two excitation wavelengths resonantly address complementary chirality sets, so a single plate yields multiple independent optical channels instead of one aggregate signal:

| Excitation | Chiralities addressed |
|---|---|
| 655 nm | (7,5) · (7,6) |
| 735 nm | (10,2) · (9,4) · (8,6) · (8,7) |

LabVIEW handles plate traversal, excitation switching, exposure triggering, and file naming, writing one spectrum per well per excitation wavelength. Automating acquisition at this layer is what makes unattended multi-plate operation possible and removes operator timing from the measurement entirely.

---

## Stage 4 — Spectral preprocessing and deconvolution

Raw well spectra contain overlapping emission from several chiralities at once, so individual contributions must be separated before any response can be quantified.

1. **Background correction** — removal of baseline and scattering contributions
2. **Smoothing** — Savitzky-Golay filtering, preserving peak shape while suppressing detector noise
3. **Segmentation** — dataset split by excitation wavelength (655 nm / 735 nm channels)
4. **Lorentzian deconvolution** — nonlinear least-squares fitting of overlapping peaks, optimizing full width at half maximum, peak position, and intensity to resolve each chirality
5. **Replicate aggregation** — triplicates combined per DNA × condition, with mean and standard deviation retained

Fit residuals are kept and inspected. A poor fit is itself a data-quality signal — wells that fail fitting are flagged rather than silently averaged into the result.

Implementation: [`PL_Preprocessing_Deconvolution/`](./PL_Deconvolution_PL_Preprocessing)

---

## Stage 5 — Response extraction

From the deconvoluted peaks, two metrics are computed **per chirality, per sequence**, each relative to its paired PBS blank:

- **Intensity change** — ΔI/I₀
- **Peak shift** — Δλ

This yields **six chirality-resolved channels** — (7,5), (7,6), (10,2), (9,4), (8,6), (8,7) — for every sequence screened. Different chiralities respond differently to the same analyte, so keeping them separate preserves information that averaging into a single scalar would destroy. In the glucose campaign, **(7,6) and (9,4) showed the significant intensity changes** and were carried forward as the response channels of interest.

Output is a tabular, model-ready dataset:

```
sequence · chirality · analyte · ΔI/I₀ · Δλ · replicate mean/SD · plate/well provenance
```

Implementation: [`Response_Extraction/`](./Response_Extraction)

---

## Repository contents

| Folder | Contents |
|---|---|
| [`PL_Preprocessing_Deconvolution/`](./PL_Deconvolution_PL_Preprocessing) | Background correction, Savitzky-Golay smoothing, wavelength-channel segmentation, and Lorentzian peak deconvolution for the 655 nm and 735 nm channels |
| [`Response_Extraction/`](./Response_Extraction) | ΔI/I₀ and Δλ computation per chirality against paired blanks, replicate statistics, and export of the ML-ready response table |

---

## Toward a closed automated loop

Acquisition is already automated at the instrument layer (LabVIEW + LightField). The direction of development is to close the remaining gaps so design, preparation, measurement, and processing run as one continuous cycle:

- **Preparation** — robotic liquid handling for the exchange protocol, resuspension, normalization, and plate assembly
- **Acquisition** — unattended multi-plate operation with automated in-line quality control
- **Processing** — hands-off execution of deconvolution and response extraction as measurement completes
- **Orchestration** — a single controller sequencing all three, capturing full provenance per well

The constraint this addresses is **replicate variance rather than raw throughput**. The manual protocol involves many timing-sensitive steps — sonication, staggered additions, fixed centrifugation and rest intervals — where small operator-to-operator drift accumulates into label noise. The resolution of any downstream model is bounded by the precision of the labels this pipeline produces, so reducing that variance is worth more than simply running more plates.

---

## Reference

Rabbani, Y., Bregy, J., Rousseau, B., Sajjadi, S. H., De Benedittis, L., Behjati, S., Mouhib, M., Dehury, S., Boghossian, A. A. *"Discovery of a DNA-based Optical Nanotube Sensor for Glucose Using Clustering and Deep Learning Algorithms."* bioRxiv, 2025. [doi:10.1101/2025.05.06.652529](https://doi.org/10.1101/2025.05.06.652529)

Related to European Patent Application EP:24211885.9.
