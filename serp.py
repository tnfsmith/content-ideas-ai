import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import math

def search_google_requests(query, num_results):
    # Enforce limits on num_results
    num_results = min(max(num_results, 5), 100)

    # Calculate the number of pages
    n_pages = math.ceil(num_results / 10)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    results = []
    counter = 0
    for page in range(1, n_pages + 1):
        url = f"http://www.google.com/search?q={query}&start={(page - 1) * 10}"

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        search = soup.find_all("div", class_="yuRUbf")

        for h in search:
            if counter == num_results:
                break
            counter += 1
            title_element = h.find("h3")
            if title_element:
                title = title_element.text
                link = h.a.get("href")
                rank = counter
                results.append(
                    {
                        "title": title,
                        "url": link,
                        "domain": urlparse(link).netloc,
                        "rank": rank,
                    }
                )

            if counter == num_results:
                break

    return results
