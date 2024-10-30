# Hong Kong Gazette Document Downloader

A command-line tool to search and download gazette documents from the Hong Kong government website.

## Features

- Search for gazette documents by year and query
- Automatically download PDF documents
- Organize downloaded files with a consistent naming convention
- Concurrent downloads with retry functionality
- Rate limiting to respect server resources
- Interactive progress bar

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/qiuhaohao/hk-gov-gazette-download.git
   cd hk-gov-gazette-download
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
python main.py -y YEAR1 -y YEAR2 -q "QUERY" -o OUTPUT_DIRECTORY [OPTIONS]
```

Options:
- `-y`, `--years`: Years to search (can be specified multiple times)
- `-q`, `--query`: Search query
- `-o`, `--output`: Output directory for downloaded PDFs
- `-r`, `--retry`: Number of retry attempts for failed downloads (default: 3)
- `-w`, `--max-workers`: Maximum number of concurrent downloads (default: 10)
- `-l`, `--language`: Language (default: chinese)

### Examples
#### Chinese search
```sh
python main.py -y 2024 -y 2023 -q "公司註冊處處長" -o output_pdfs
```
This searches for Chinese documents from 2023 and 2024 with the query "公司註冊處處長" and downloads PDFs to "./output_pdfs".
#### English search
```sh
python main.py -y 2024 -y 2023 -q "Registrar of Companies" -o output_pdfs -l english
```
This searches for English documents from 2023 and 2024 with the query "Registrar of Companies" and downloads PDFs to "./output_pdfs".

## Search PDFs

./scripts/pdfmatch script can be used to search for one single capturing group in a pdf file.
```sh
$ ./scripts/pdfmatch "Pursuant to section (.+) of the Companies Ordinance" output_pdfs/2024-28-1-0-0-53-english.pdf
output_pdfs/2024-28-1-0-0-53-english.pdf        745(2)(b)
```

To calculate the frequency of each section under Companies Ordinance, you can use the following command:
```sh
$ find output_pdfs -name "*.pdf" -exec ./scripts/pdfmatch "section (.+?) of the Companies Ordinance" {} \; | awk '{print $2}' | sort | uniq -c | sort -nr
    489 762
    255 751(3)
    240 751(1)
    183 767(7)
     83 110(5)(b)
     45 745(2)(b)
     17 746(2)
     16 753
      3 772(5)(b)
      2 796(3)
      1 797(2)(b)
```
