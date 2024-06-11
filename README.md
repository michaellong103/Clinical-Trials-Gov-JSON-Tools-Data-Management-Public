## Overview

ClinicalTrials.gov Data Management Tools for AI projects.

[My Portfolio](https://pm.mikeylong.com)  

# Clinical Trials Data Management Program - Pub

This program automates downloading, extracting, processing, and analyzing JSON clinical trial data from ClinicalTrials.gov. It provides a command-line interface (CLI) for various tasks related to clinical trial data management and usage with AI models.

## Functionality

### 1. Download the ZIP file (download.py)

- **Description**: Downloads a ZIP file containing clinical trial data from ClinicalTrials.gov.
- **Steps**:
  - Executes `download.py` to fetch the ZIP file.
  - Saves the ZIP file to the `data/raw` directory.

### 2. Extract ZIP file contents (extract_zip.py)

- **Description**: Extracts contents of the downloaded ZIP file.
- **Steps**:
  - Runs `extract_zip.py`.
  - Extracts files into the `data/raw/extracted` directory.

### 3. Recommend clinical trials (gpt_recommendation.py)

- **Description**: Uses a GPT model to recommend clinical trials based on the processed data.
- **Steps**:
  - Executes `gpt_recommendation.py`.
  - Analyzes processed data and generates recommendations.

### 4. Clean and process JSON files (clean_files.py)

- **Description**: Cleans and processes JSON files by removing unnecessary information and organizing data.
- **Steps**:
  - Runs `clean_files.py`.
  - Reads JSON files from `data/processed`.
  - Saves cleaned data to `data/cleaned`.

### 5. Delete JSON files (delete_json_files.py)

- **Description**: Deletes JSON files to free up space or remove outdated data.
- **Steps**:
  - Runs `delete_json_files.py`.
  - Deletes JSON files from specified directories.

### 6. Randomly split data (split_out_random.py)

- **Description**: Randomly splits clinical trial data into training and testing sets.
- **Steps**:
  - Runs `split_out_random.py`.
  - Saves split data into appropriate directories.

### 7. Filter and process data by condition (split_out_condition.py)

- **Description**: Filters and processes data based on a specified condition (e.g., "Breast Cancer").
- **Steps**:
  - Runs `split_out_condition.py` with specified arguments.
  - Extracts and filters data based on the condition.
  - Saves filtered data to the output directory.

### 0. Exit the program

- **Description**: Exits the program.
- **Steps**:
  - Exits the CLI loop and terminates the program.

## Usage Instructions

1. **Run the Program**:
   - Execute `app.py` to start the CLI interface.
   - `python3 app.py`

2. **Select an Option**:
   - Follow prompts to select an available option.
   - Enter the number corresponding to the task you want to perform.

3. **Follow Prompts**:
   - Provide necessary input for tasks requiring additional information.

4. **Monitor Output**:
   - Monitor console messages for task progress and relevant information.

5. **Exit**:
   - Select option `0` to exit the program when finished.

## Example Usage

To filter and process clinical trial data based on the condition "HIV":

1. Run the program:
   - `python3 app.py`
2. Select option `7`:
   - `Enter the number of the command you want to run: 7`
3. Enter the condition:
   - `Enter the condition to filter by (e.g., 'Breast Cancer'): HIV`
4. Follow prompts to complete the task.

## Prerequisites

Ensure you have the following installed:

- Python 3.6 or later
- Necessary Python packages listed in `requirements.txt`

Install required packages using pip:

```bash
pip install -r requirements.txt
