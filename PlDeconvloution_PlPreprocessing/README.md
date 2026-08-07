# Photoluminescence-PL-Data-Preprocessing-and-Deconvolution (2022-2024)

## Overview
This repository provides a comprehensive pipeline for preprocessing and analyzing **photoluminescence (PL) spectra** data, derived from experiments using nanobiosensors for different analyte detection. The data comes from a custom-built optical setup, and this repository includes scripts for preprocessing, deconvolution, and visualization of the PL spectra, enabling detailed analysis of single-walled carbon nanotube (SWCNT) chirality.

### Purpose
The main objective of this repository is to preprocess PL spectrum data to remove background noise, smooth the data, and deconvolute overlapping spectral peaks. This pipeline can be applied to datasets for a variety of analytes detected by nanobiosensors.

Key features of this repository include:
- Loading and processing multiple CSV files with PL spectrum data.
- Background correction, noise removal, and data smoothing using the **Savitzky-Golay filter**.
- Lorentzian peak deconvolution for resolving overlapping spectral peaks.
- Visualization of the processed PL data and spectral features for further analysis.

---

## Technologies and Tools Used
- **Python**: The primary programming language used for data preprocessing, deconvolution, and visualization.
- **NumPy & Pandas**: For handling data matrices and manipulating CSV files.
- **Matplotlib**: For generating plots of PL intensity, individual peaks, and fitted spectra.
- **SciPy**: Used for nonlinear least-squares optimization in the Lorentzian peak deconvolution process.

---

## Key Project Highlights

### 1. Photoluminescence (PL) Spectrum Analysis
The PL data was captured using a custom-built optical N-IR microscope setup.
- **Excitation wavelengths**: 660 nm for the (7,5) and (7,6) chiralities, and 730 nm for the (10,2), (9,4), (8,6), and (8,7) chiralities.
- **Emission range**: 900 to 1400 nm, captured using an IsoPlane SCT-320 spectrometer with a NIRvana 640 ST InGaAs camera.

The Python code processes PL spectrum data by:
- Loading multiple CSV files into a matrix.
- Applying background correction to remove noise.
- Smoothing the data with a **Savitzky-Golay filter**.
- Dividing the data based on excitation wavelength (660 nm and 730 nm).
- Saving the processed datasets and generating visual plots of PL intensity.
- Optionally calculating the **area under the curve (AUC)** for quantitative analysis of intensity variations.

### 2. Deconvolution of Photoluminescence Spectra
The **Lorentzian peak deconvolution** is applied to resolve overlapping spectral features:
- Peak fitting is performed using Lorentzian functions for the (7,5) and (7,6) chiralities at 660 nm, and (10,2), (9,4), (8,6), and (8,7) chiralities at 730 nm.
- The script uses **nonlinear least-squares optimization** to iteratively adjust peak parameters (FWHM, peak center, and intensity) to achieve the best fit.

The deconvolution script produces:
- Fitted peak parameters for each spectrum.
- Visual plots showing individual fitted peaks, combined spectra, and residuals to assess the fit quality.
- Export of fitted parameters in CSV format for further analysis.


### 3. DNA Sensor Data Analysis for specific Analytes

This repository contains Python code for analyzing DNA sensor data related to glucose detection. It includes scripts for calculating means, standard deviations, peak shifts, and intensity changes across various DNA samples and channels. The results are visualized as bar plots, and the processed data is exported as Excel files. The code is designed for analyzing time-series data from DNA sensor experiments, focusing on glucose concentration measurements.



## Repository Structure

[#repository-structure](#repository-structure)

The repository consists of three standalone Python scripts:

1. **`Preprocessing_of_Pl_Spectrum.py`** — Loads raw PL spectrum CSV files, applies background correction and Savitzky-Golay smoothing, splits data by excitation wavelength (660 nm / 730 nm), and optionally computes area-under-curve (AUC) for intensity analysis.
2. **`Deconvolution-of-Photoluminescence-PL-Spectra-660.py`** — Lorentzian peak deconvolution for the 660 nm excitation channel, resolving the (7,5) and (7,6) SWCNT chiralities via nonlinear least-squares fitting.
3. **`Deconvolution-of-Photoluminescence-PL-Spectra-730.py`** — Lorentzian peak deconvolution for the 730 nm excitation channel, resolving the (10,2), (9,4), (8,6), and (8,7) SWCNT chiralities.

Each script is self-contained and can be run independently on your own PL spectrum CSV files (update the input file path at the top of each script).

---

## How to Use the Preprocessing Pipeline

[#how-to-use-the-preprocessing-pipeline](#how-to-use-the-preprocessing-pipeline)

### 1. Data Preparation

[#1-data-preparation](#1-data-preparation)

- Export your raw PL spectrum data as CSV, with wavelength and intensity columns.
- Update the file path variable at the top of `Preprocessing_of_Pl_Spectrum.py` to point to your CSV file(s).

### 2. Preprocessing

[#2-preprocessing](#2-preprocessing)

- Run `Preprocessing_of_Pl_Spectrum.py` to apply background correction, Savitzky-Golay smoothing, and split data by excitation wavelength. Processed output is saved to CSV in the same directory.

### 3. Deconvolution

[#3-deconvolution](#3-deconvolution)

- Run `Deconvolution-of-Photoluminescence-PL-Spectra-660.py` or `-730.py` (matching your excitation wavelength) on the preprocessed data to fit Lorentzian peaks and resolve overlapping chirality signals.
- Each script outputs fitted peak parameters (FWHM, center, intensity) as CSV, plus plots of individual peaks, combined spectra, and fit residuals.
---

## How to Use the Preprocessing Pipeline

### 1. Data Preparation
- Ensure that your PL spectrum data is in CSV format and organized as described in the `/data` directory.
- Raw data can be uploaded into the pipeline for background correction and smoothing.

### 2. Running the Preprocessing Script
- Use the Python scripts located in the `/scripts` directory to preprocess the PL spectrum data. Run the main script to load the data, apply background correction, and perform deconvolution.
- The script also allows for filtering data based on excitation wavelength and saving the processed results in CSV format.

### 3. Visualization and Analysis
- Open the Jupyter Notebooks in the `/notebooks` directory for an interactive walkthrough of the data preprocessing steps.
- The notebooks provide a step-by-step guide for loading the data, visualizing the PL spectra, and applying deconvolution.

### 4. Saving the Results
- Processed data, plots, and results are saved in the `/results` directory. These include fitted parameters, visual plots of the spectra, and quantitative analysis results such as AUC calculations.

---

