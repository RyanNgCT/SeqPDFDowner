import requests
import os, sys
from dotenv import load_dotenv

def getVars() -> tuple[str, str]:
    """
    Retrieves environment variables from .env file.
    """
    base_url = os.getenv('BASE_URL')
    cookie = os.getenv('COOKIE')

    return base_url, cookie

def recursivePDFDownload(base_url: str, cookie: str, naming: str, start: int, stop: int):
    """
    Download PDFs in incremental order.
        - base_url <str>: Base URL of the PDFs to download.
        - cookie <str>: User cookie obtained from the getVars() method.
        - naming <str>: Prefix name for the PDF document.
        - start <int>: Start index of PDFs to download.
        - stop <int>: Stop index of PDFs to download (last document filename).
    """

    headers = {
        'Cookie': cookie,
        'Content-Type': 'application/pdf',
        'Connection': 'keep-alive'
    }
    timeout_seconds = 30
    download_dir = 'downloaded'

    # Create the directory if it doesn't exist
    os.makedirs(download_dir, exist_ok=True)

    for i in range(start, stop + 1):  # include stop index
        file_index = f'{i:02}'

        try:
            response = requests.get(f'{base_url}{file_index}.pdf', headers=headers, timeout=timeout_seconds)
            response.raise_for_status() 

            file_path = os.path.join(download_dir, f'{naming}{file_index}.pdf')
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f'{file_path} downloaded successfully')
        except requests.exceptions.RequestException as e:
            print(f'Failed to download file {naming}{file_index}.pdf. Error: {e}')

if __name__ == '__main__':
    load_dotenv()
    base_url, cookie = getVars()
    try:
        indices = input("Enter start and stop indices to download (inclusive): ")
        start, stop = map(int, indices.split(','))  # Split input by comma and convert to ints
    except ValueError:
        sys.exit("Invalid input. Run the program again!")
    else:
        naming = input("Enter a prefix naming convention: ")
        recursivePDFDownload(base_url, cookie, naming, start, stop)
