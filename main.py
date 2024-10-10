import click
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs
import os
from typing import List
from tqdm import tqdm
import time
import logging
import threading
import concurrent.futures

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Global rate limiter
class RateLimiter:
    def __init__(self, max_calls, period):
        self.max_calls = max_calls
        self.period = period
        self.calls = []
        self.lock = threading.Lock()

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            with self.lock:
                now = time.time()
                self.calls = [t for t in self.calls if now - t < self.period]
                if len(self.calls) >= self.max_calls:
                    sleep_time = self.period - (now - self.calls[0])
                    time.sleep(sleep_time)
                self.calls.append(time.time())
            return func(*args, **kwargs)
        return wrapper

rate_limiter = RateLimiter(max_calls=30, period=1)

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

@rate_limiter
def download_pdf(url: str, output_dir: str, retry_count: int) -> None:
    parsed_url = urlparse(url)
    params = parse_qs(parsed_url.query)
    
    filename = f"{params['year'][0]}-{params['vol'][0]}-{params['no'][0]}-{params['extra'][0]}-{params['type'][0]}-{params['number'][0]}.pdf"
    filepath = os.path.join(output_dir, filename)
    
    for attempt in range(retry_count):
        try:
            response = requests.get(url)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            return filename
        except requests.RequestException as e:
            if attempt < retry_count - 1:
                logging.warning(f"Attempt {attempt + 1} failed for {filename}. Retrying... Error: {str(e)}")
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                logging.error(f"Failed to download {filename} after {retry_count} attempts. Error: {str(e)}")
                return None

@click.command()
@click.option('--years', '-y', multiple=True, type=int, required=True, help='Years to search for (can be specified multiple times)')
@click.option('--query', '-q', required=True, help='Search query')
@click.option('--output', '-o', required=True, type=click.Path(), help='Output directory for downloaded PDFs')
@click.option('--retry', '-r', default=3, help='Number of retry attempts for failed downloads')
@click.option('--max-workers', '-w', default=10, help='Maximum number of concurrent downloads')
def main(years, query, output, retry, max_workers):
    """Download gazette documents from the Hong Kong government website."""
    os.makedirs(output, exist_ok=True)

    
    print(f"Searching for documents with query: '{query}' for years: {', '.join(map(str, years))}")
    links = get_gazette_links(list(years), query)
    print(f"Found {len(links)} documents")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_link = {executor.submit(download_pdf, link, output, retry): link for link in links}
        
        with tqdm(total=len(links), desc="Downloading", unit="file") as pbar:
            for future in concurrent.futures.as_completed(future_to_link):
                link = future_to_link[future]
                try:
                    result = future.result()
                    if result:
                        pbar.set_postfix_str(f"Current: {result}", refresh=True)
                    pbar.update(1)
                except Exception as e:
                    logging.error(f"An error occurred for {link}: {str(e)}")
    
    print(f"All documents downloaded to: {output}")

if __name__ == "__main__":
    main()
