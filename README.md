## Overview

ClinicalTrials.gov Data Management Tools for AI projects.

[My Portfolio](https://pm.mikeylong.com)  

# Clinical Trials Data Management Program - Pub

This program automates downloading, extracting, processing, and analyzing JSON clinical trial data from ClinicalTrials.gov. It provides a command-line interface (CLI) for various tasks related to clinical trial data management and usage with AI models.

##  ##################################################

# Clinical Trial Data Processing Workflow

Using .md and .csv Files to Create Vector Stores for OpenAI
The project scripts facilitate the transformation of raw clinical trial data into Markdown (.md) and CSV (.csv) files, which can then be uploaded to a vector store in the OpenAI dashboard. The json_to_md.py script converts cleaned JSON data into Markdown files, making the data easily readable and accessible for documentation purposes. Simultaneously, the json_to_csv.py script transforms the cleaned data into CSV format, which is highly suitable for structured data analysis and machine learning workflows.

Once converted, these .md and .csv (as txt) files can be uploaded directly to the OpenAI dashboard to create vector stores. These vector stores allow OpenAI's powerful language models to efficiently perform similarity searches and other natural language processing tasks, leveraging the organized and well-structured data from clinical trials. This process not only streamlines data management but also enhances the ability to draw insights and conduct detailed analysis using OpenAI's advanced AI capabilities.

##   ########################################################################################
Getting Started
##   ########################################################################################

## Getting Started

This guide will help you set up your environment and get started with processing clinical trial data. Follow the steps below to install dependencies, set up your environment, and run the scripts.

### Prerequisites

1. **Miniconda**: Miniconda is a minimal installer for conda, a package manager for Python and R. It helps to create isolated environments for different projects, ensuring dependency conflicts are minimized.

2. **Python Version**: The project is compatible with Python 3.9 and above. Make sure you have the appropriate Python version installed.

3. **Git**: Git is a version control system that helps manage code changes. It is essential for downloading the project repository and managing updates.

4. **API Keys**: Some scripts require API keys, such as the OpenAI API key. Ensure you have the necessary API keys set up.

### Installation Steps

#### Step 1: Install Miniconda

Download and install Miniconda from the official website: [Miniconda Download](https://docs.conda.io/en/latest/miniconda.html)

For macOS:
\`\`\`bash

# bash Miniconda3-latest-MacOSX-x86_64.sh

\`\`\`
Follow the prompts to complete the installation.

#### Step 2: Create a Conda Environment

Create a new conda environment for the project:
\`\`\`bash

# conda create -n clinical-trials python=3.9

# conda activate clinical-trials

\`\`\`

#### Step 3: Clone the Repository

Clone the project repository using Git:
\`\`\`bash

# git clone <https://github.com/your-username/clinical-trials.git>

# cd clinical-trials

\`\`\`

#### Step 4: Install Dependencies

Install the required Python packages using the \`requirements.txt\` file:
\`\`\`bash

# pip install -r requirements.txt

\`\`\`

### Dependencies

* **requests**: A simple HTTP library for Python, used for making HTTP requests.
  \`\`\`bash

# pip install requests

  \`\`\`

* **tqdm**: A library for adding progress bars to Python loops.
  \`\`\`bash

# pip install tqdm

  \`\`\`

* **openai**: The OpenAI library is used to interact with OpenAI's GPT-3 model.
  \`\`\`bash

# pip install openai

  \`\`\`

### Setting Up API Keys

Some scripts require API keys to access external services. For example, the \`openai\` package needs an API key for OpenAI's GPT-3. Set up your API keys as environment variables:

1. **OpenAI API Key**:
   \`\`\`bash

# export OPENAI_API_KEY='your-api-key'

   \`\`\`

### Running the Scripts

After setting up the environment and installing dependencies, you can start running the scripts. Below are some examples:

#### Download the ZIP File

Run the \`download.py\` script to download the clinical trial data:
\`\`\`bash

# python download.py

\`\`\`

#### Extract ZIP File Contents

Run the \`extract_zip.py\` script to extract the contents of the downloaded ZIP file:
\`\`\`bash

# python extract_zip.py

\`\`\`

#### Clean and Process JSON Files

Run the \`clean_files.py\` script to clean and process the JSON files:
\`\`\`bash

# python clean_files.py

\`\`\`

#### Filter Data by Condition

Run the \`split_out_condition.py\` script to filter data based on a specific condition:
\`\`\`bash

# python split_out_condition.py "Breast Cancer"

\`\`\`

### Summary

Each directory in the \`data/\` structure serves a specific purpose in the data processing pipeline, ensuring the data is transformed, cleaned, and stored in the appropriate format for further analysis and use. The workflow moves data from raw downloads to extracted files, processed and cleaned datasets, and finally to various output formats like CSV, Markdown, and Parquet for different use cases.

Save the above content as \`README.md\` in your project directory.

##   ########################################################################################

Process
##   ########################################################################################

## Graph of process

    A[Download ZIP file] --> B[Extract ZIP file contents];
    B --> C1[Clean and process JSON files];
    B --> C2[Filter data by condition];
    C1 --> D1[Convert JSON files to CSV];
    C1 --> D2[Convert JSON files to Markdown];
    D1 --> E1[Create JSON for LangChain];
    D2 --> E2[Create Parquet for LangChain];

    A[download.py] -->|Downloads clinical trial data ZIP| B[extract_zip.py];
    B[extract_zip.py] -->|Extracts contents of downloaded ZIP| C1[clean_files.py];
    B[extract_zip.py] -->|Filters and processes by condition| C2[split_out_condition.py];
    C1[clean_files.py] -->|Converts cleaned JSON to CSV| D1[json_to_csv.py];
    C1[clean_files.py] -->|Converts cleaned JSON to Markdown| D2[json_to_md.py];
    D1[json_to_csv.py] -->|Creates JSON compatible with LangChain| E1[langchain_create_json.py];
    D2[json_to_md.py] -->|Creates Parquet for LangChain| E2[langchain_create_parquet.py];

## Steps for the Clinical Trial Data Processing Workflow

### Step 1: Download the ZIP File

**Filename:** `download.py`

**Description:** Downloads the ZIP file containing clinical trial data from ClinicalTrials.gov.

**Input Directory:** N/A

**Output Directory:** `data/raw`

**How it works:**

* The script downloads a ZIP file from a specified URL and saves it to the `data/raw` directory.
* It uses the `requests` library to stream the download and the `tqdm` library to display a progress bar.

---

### Step 2: Extract ZIP File Contents

**Filename:** `extract_zip.py`

**Description:** Extracts contents of the downloaded ZIP file.

**Input Directory:** `data/raw`

**Output Directory:** `data/extracted`

**How it works:**

* The script verifies if the ZIP file is valid and then extracts its contents into the `data/extracted` directory.
* It uses the `zipfile` library to handle ZIP file operations.

---

### Step 3a: Clean and Process JSON Files

**Filename:** `clean_files.py`

**Description:** Cleans and processes JSON files by extracting necessary information and saves them in the cleaned directory.

**Input Directory:** `data/processed`

**Output Directory:** `data/cleaned`

**How it works:**

* The script reads JSON files from the `data/processed` directory, extracts relevant data fields, and saves the cleaned data to the `data/cleaned` directory.
* It uses the `json` library for reading and writing JSON data.

**Why it's different from Step 3b:**

* **Purpose:** Step 3a is focused on cleaning the data by extracting necessary fields and reformatting the data for further use.
* **Data Handling:** It processes all JSON files to extract and clean the core clinical trial information.

---

### Step 3b: Filter Data by Condition

**Filename:** `split_out_condition.py`

**Description:** Filters and processes JSON files based on a specified condition.

**Input Directory:** `data/extracted`

**Output Directory:** `data/processed`

**How it works:**

* The script reads JSON files from the `data/extracted` directory, filters the data based on a specified condition (e.g., "Breast Cancer"), and saves the filtered data to the `data/processed` directory.
* It uses the `json` library for JSON operations and `argparse` for command-line arguments.

**Why it's different from Step 3a:**

* **Purpose:** Step 3b is designed to filter and categorize data based on specific conditions, making it easier to focus on particular subsets of the data.
* **Data Handling:** It selectively filters data based on conditions and saves only the relevant subsets, which can then be used for condition-specific analysis.

---

### Step 4a: Convert JSON Files to CSV

**Filename:** `json_to_csv.py`

**Description:** Converts JSON files in the cleaned directory to CSV files in the CSV directory.

**Input Directory:** `data/cleaned`

**Output Directory:** `data/csv`

**How it works:**

* The script reads JSON files from the `data/cleaned` directory, converts them to CSV format, and saves the CSV files in the `data/csv` directory.
* It uses the `pandas` library for data manipulation and conversion.

---

### Step 4b: Convert JSON Files to Markdown

**Filename:** `json_to_md.py`

**Description:** Converts JSON files in the cleaned directory to Markdown files in the MD directory.

**Input Directory:** `data/cleaned`

**Output Directory:** `data/md`

**How it works:**

* The script reads JSON files from the `data/cleaned` directory, converts them to Markdown format, and saves the Markdown files in the `data/md` directory.
* It uses the `pandas` library to handle data normalization and conversion to Markdown.

---

### Step 5a: Create JSON for LangChain

**Filename:** `langchain_create_json.py`

**Description:** Processes the cleaned JSON files to create a JSON format compatible with LangChain for vector storage and search.

**Input Directory:** `data/cleaned`

**Output Directory:** `data/vector_store/json`

**How it works:**

* The script reads JSON files from the `data/cleaned` directory, processes the content for vector storage, and adds them to a vector store using the LangChain library.
* It uses the `openai` and `langchain_community` libraries for embedding and vector storage.

---

### Step 5b: Create Parquet for LangChain

**Filename:** `langchain_create_parquet.py`

**Description:** Processes the cleaned JSON files to create a Parquet format compatible with LangChain for vector storage and search.

**Input Directory:** `data/apache_parquet`

**Output Directory:** `data/vector_store/parquet`

**How it works:**

* The script reads Parquet files from the `data/apache_parquet` directory, processes the content for vector storage, and adds them to a vector store using the LangChain library.
* It uses the `pandas`, `openai`, and `langchain_community` libraries.

---

## Summary of the Process

1. **Step 1:** Download ZIP file (`download.py`)
2. **Step 2:** Extract ZIP file contents (`extract_zip.py`)
3. **Step 3a:** Clean and process JSON files (`clean_files.py`)
4. **Step 3b:** Filter data by condition (`split_out_condition.py`)
5. **Step 4a:** Convert JSON files to CSV (`json_to_csv.py`)
6. **Step 4b:** Convert JSON files to Markdown (`json_to_md.py`)
7. **Step 5a:** Create JSON for LangChain (`langchain_create_json.py`)
8. **Step 5b:** Create Parquet for LangChain (`langchain_create_parquet.py`)

---

## What type of data is in each directory under `data/`

### `data/raw`

**Contents:**

* Raw data files directly downloaded from the source, such as ZIP files containing clinical trial data from ClinicalTrials.gov.

**Examples:**

* `AllAPIJSON.zip` - The downloaded ZIP file containing all the clinical trial JSON data.

### `data/extracted`

**Contents:**

* Extracted files from the ZIP archive. These are raw JSON files that have been unzipped but not yet processed.

**Examples:**

* `AllAPIJSON` directory containing multiple JSON files.

### `data/processed`

**Contents:**

* JSON files that have been filtered and processed based on specific conditions (e.g., filtering by a specific disease or condition).

**Examples:**

* Filtered JSON files categorized by conditions such as "Breast Cancer".

### `data/cleaned`

**Contents:**

* Cleaned JSON files that have been processed to extract relevant fields and format the data appropriately.

**Examples:**

* Cleaned JSON files containing essential information like "BriefTitle", "EligibilityCriteria", etc.

### `data/csv`

**Contents:**

* CSV files created by converting the cleaned JSON data into a tabular format.

**Examples:**

* `clinical_trials_cleaned.csv` - A CSV file containing cleaned clinical trial data.

### `data/md`

**Contents:**

* Markdown files created by converting the cleaned JSON data into Markdown format.

**Examples:**

* `combined_0.md`, `combined_1.md`, etc. - Markdown files combining the content of several JSON files.

### `data/apache_parquet`

**Contents:**

* Parquet files containing cleaned and processed data stored in Apache Parquet format, suitable for efficient data storage and retrieval.

**Examples:**

* Parquet files generated from cleaned JSON data.

### `data/vector_store/json`

**Contents:**

* JSON files formatted and processed for use with LangChain's vector storage system.

**Examples:**

* JSON files containing embedded text data for similarity searches.

### `data/vector_store/parquet`

**Contents:**

* Parquet files formatted and processed for use with LangChain's vector storage system.

**Examples:**

* Parquet files containing embedded text data for similarity searches.

---

## Summary

Each directory in the `data/` structure serves a specific purpose in the data processing pipeline, ensuring the data is transformed, cleaned, and stored in the appropriate format for further analysis and use. The workflow moves data from raw downloads to extracted files, processed and cleaned datasets, and finally to various output formats like CSV, Markdown, and Parquet for different use cases.

##   ########################################################################################

Tools
##   ########################################################################################

## create_embeddings.py

**Description:** This script generates embeddings for the text data from clinical trial files using OpenAI's Embedding API. These embeddings are used for tasks like similarity searches or other machine learning tasks.

* **Input Directory:** `data/cleaned`
* **Output Directory:** `data/embeddings`

**Why You Need It:**
Embeddings convert text data into numerical vectors, which are essential for various natural language processing tasks. These vectors enable the system to perform similarity searches and other analyses efficiently.

## test_LangChain.py

**Description:** This script loads JSON files, processes the text data to generate embeddings using OpenAI's API, and stores these embeddings in a vector store for later retrieval.

* **Input Directory:** `data/cleaned`
* **Output Directory:** None specified directly; it interacts with the vector store.

**Why You Need It:**
This script is crucial for setting up and testing the vector store, ensuring that text data is correctly processed and stored for efficient retrieval and similarity search operations.

## split_out_random.py

**Description:** This script reads JSON files and splits the data randomly into training and testing datasets. It helps in creating datasets for machine learning models.

* **Input Directory:** `data/extracted`
* **Output Directory:** `data/processed/random_split`

**Why You Need It:**
Randomly splitting data into training and testing sets is essential for evaluating machine learning models. This script helps in preparing the datasets needed for training and validation.

## delete_json_files.py

**Description:** This script deletes JSON files and any empty folders within the specified directory. It helps in cleaning up the workspace by removing unnecessary files.

* **Input Directory:** Specified directory, e.g., `data`
* **Output Directory:** None (files are deleted)

**Why You Need It:**
Maintaining a clean workspace is important to manage storage and ensure that only relevant data is retained. This script helps automate the cleanup process.

## test_openai_key.py

**Description:** This script checks if the OpenAI API key is set correctly in the environment variables and prints the key if it is set.

* **Input Directory:** None
* **Output Directory:** None

**Why You Need It:**
Validating that the API key is correctly set up is crucial for scripts that rely on OpenAI services. This script ensures that the API key is accessible and correctly configured.

## status.py

**Description:** This script provides a summary report of the directory structure and the status of files in various directories. It helps in monitoring the status of data files and directories.

* **Input Directory:** Base directory, typically the root project directory
* **Output Directory:** Prints summary to console

**Why You Need It:**
Regularly checking the status of data files and directories helps in managing the workflow and ensuring that all steps of the data processing pipeline are functioning as expected. This script aids in monitoring and reporting.

---

These tools are essential for managing, processing, and analyzing clinical trial data efficiently. Each script has a specific role in the data processing pipeline, from downloading and extracting data to cleaning, embedding, and preparing datasets for machine learning tasks.

