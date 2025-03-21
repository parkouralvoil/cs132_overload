import requests
from bs4 import BeautifulSoup
import os
import urllib.parse

# cd data gas
# python -m NCR_pump_prices_download

def download_doe_pdf(url: str, save_directory: str ="doe_pdfs") -> None:
    """
    Downloads all PDF files from the given DOE website URL.

    Args:
        url (str): The URL of the DOE website.
        save_directory (str): The directory to save the downloaded PDFs.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        soup = BeautifulSoup(response.content, "html.parser")

        # Find all anchor tags with href attributes ending in .pdf
        pdf_links = [a["href"] for a in soup.find_all("a", href=lambda href: href and href.endswith(".pdf"))]

        if not os.path.exists(save_directory):
            os.makedirs(save_directory)

        for link in pdf_links:
            # Handle relative and absolute URLs
            if not link.startswith("http"):
                link = urllib.parse.urljoin(url, link) #join the base url with the relative link

            filename = os.path.join(save_directory, link.split("/")[-1])

            try:
                pdf_response = requests.get(link, stream=True) #stream = true is for large files
                pdf_response.raise_for_status()

                with open(filename, "wb") as f:
                    for chunk in pdf_response.iter_content(chunk_size=8192): #chunk size is 8KB
                        f.write(chunk)
                print(f"Downloaded: {filename}")

            except requests.exceptions.RequestException as pdf_e:
                print(f"Error downloading {link}: {pdf_e}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
    except Exception as general_e:
        print(f"An unexpected error occured: {general_e}")

if __name__ == "__main__":
    for i in range(1, 42):
        doe_url = f"https://doe.gov.ph/retail-pump-prices-metro-manila?page={i}"
        download_doe_pdf(doe_url)
