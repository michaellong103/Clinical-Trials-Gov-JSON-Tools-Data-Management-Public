# Automated Batch Processing

This directory contains scripts for an automated batch processing workflow. The goal is to handle JSON data files through a series of steps, from copying and splitting to cleaning and uploading to an OpenAI Vector Store.

## Directory Structure

- `app_batch.py`: Main script to run the batch processing menu.
- `conditions.json`: Configuration file for conditions used in splitting files.
- `data_batch`: Directory to store batch data during processing.
- `step_1_copy_files.py`: Script to copy files from the 'Extracted' to the 'Processed' directory.
- `step_2_split_by_condition.py`: Script to split files into separate conditions.
- `step_3_clean_files.py`: Script to clean the separated files and include only necessary JSON data.
- `step_4_upload_to_vector_store.py`: Script to upload cleaned files to the OpenAI Vector Store.

## Usage

Run the main script `app_batch.py` to access the automated batch processing menu:

```bash
python3 app_batch.py
