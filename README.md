# Hong Kong Gazette Document Downloader

A command-line tool to search and download gazette documents from the Hong Kong government website.

## Features

- Search for gazette documents by year and query
- Automatically download PDF documents
- Organize downloaded files with a consistent naming convention

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/qiuhaohao/hk-gazette-downloader.git
   cd hk-gazette-downloader
   ```

2. Set up a virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the script with the following command:
```
python main.py -y YEAR1 -y YEAR2 -q "QUERY" -o OUTPUT_DIRECTORY
```

Options:
- `-y`, `--years`: Years to search (can be specified multiple times)
- `-q`, `--query`: Search query
- `-o`, `--output`: Output directory for downloaded PDFs

Example:
```
python main.py -y 2024 -y 2023 -q "公司註冊處處長" -o output_pdfs
```
This searches for documents from 2023 and 2024 with the query "公司註冊處處長" and downloads PDFs to "./output_pdfs".
