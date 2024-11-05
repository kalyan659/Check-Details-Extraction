# Check Details Extraction using Python and Tesseract OCR
Bank check processing like check date, check number and check amount


## Introduction

This Python-based application leverages Tesseract OCR to extract essential details from check images or PDF files. The extracted data is organized into a CSV file for easy reference and analysis. A user-friendly GUI interface is provided to visualize the extracted information.

## Features

*Image and PDF Support: Accepts both image and PDF formats as input.
*Tesseract OCR Integration: Employs Tesseract OCR engine for accurate text recognition.
Data Extraction: Extracts key details such as check number, date and amount.
CSV File Generation: Organizes extracted data into a CSV file for further processing.
GUI Interface: Provides a visual interface to display extracted data.
## Install Required Libraries
Use the requirements.txt file to install required libraries. 
## Run this Script
python check simple_gui.py

## Select Input File:

Use the file dialog to choose the check image or PDF file.
## Data Extraction:

The script will process the selected file and extract relevant details.
## CSV File Generation:

The extracted data will be saved to a CSV file in the project directory.
## GUI Interface:

The GUI will display the extracted data in a tabular format.
## Configuration

Tesseract OCR: Ensure Tesseract OCR is installed and configured on your system.

## Additional Notes

For optimal results, ensure clear and well-lit check images or PDFs.
