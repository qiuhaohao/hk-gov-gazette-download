import click
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
import os
from typing import List

def get_gazette_links(years: List[int], query: str) -> List[str]:
    base_url = "https://www.gld.gov.hk/egazette/tc_chi/search_gazette/search.php"
    
    params = {
        "Years[]": years,
        "NoticeNo": "",
        "Title": query,
        "type": "mg",
        "submit": "搜尋"
    }
    
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    gazette_links = set()
    for link in soup.find_all('a', href=lambda href: href and href.startswith("../gazette/file.php")):
        relative_url = link.get('href')
        absolute_url = urljoin(response.url, relative_url)
        gazette_links.add(absolute_url)
    
    return list(gazette_links)

def download_pdf(url: str, output_dir: str) -> None:
    response = requests.get(url)
    response.raise_for_status()
    
    parsed_url = urlparse(url)
    params = parse_qs(parsed_url.query)
    
    filename = f"{params['year'][0]}-{params['vol'][0]}-{params['no'][0]}-{params['extra'][0]}-{params['type'][0]}-{params['number'][0]}.pdf"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'wb') as f:
        f.write(response.content)
    
    print(f"Downloaded: {filename}")

@click.command()
@click.option('--years', '-y', multiple=True, type=int, required=True, help='Years to search for (can be specified multiple times)')
@click.option('--query', '-q', required=True, help='Search query')
@click.option('--output', '-o', required=True, type=click.Path(), help='Output directory for downloaded PDFs')
def main(years, query, output):
    """Download gazette documents from the Hong Kong government website."""
    # Create output directory if it doesn't exist
    os.makedirs(output, exist_ok=True)
    
    print(f"Searching for documents with query: '{query}' for years: {', '.join(map(str, years))}")
    links = get_gazette_links(list(years), query)
    print(f"Found {len(links)} documents")
    
    for link in links:
        download_pdf(link, output)
    
    print(f"All documents downloaded to: {output}")

if __name__ == "__main__":
    main()
