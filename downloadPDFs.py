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
        - start <int>: First index of PDFs to download.
        - stop <int>: Last index / filename of PDFs to download.
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

    for i in range(start, stop + 1):
        file_index = f'{i:02}' # might need to modify accordingly

        try:
            response = requests.get(f'{base_url}{file_index}.pdf', headers=headers, timeout=timeout_seconds)
            response.raise_for_status()

            file_path = os.path.join(download_dir, f'{naming}{file_index}.pdf')
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f'{file_path} downloaded successfully')
        except requests.exceptions.RequestException as e:
            print(f'Failed to download file {naming}{file_index}.pdf. Error: {e}')


def testConnection(base_url: str, cookie: str, start: int) -> bool:
    """
    Tests connection to the supposed first pdf uri endpoint
        - base_url <str>: Base URL of the PDFs to download.
        - cookie <str>: User cookie obtained from the getVars() method.
        - start <int>: First index of PDFs to download.
    """

    if cookie:
        headers = {
            'Cookie': cookie,
            'Content-Type': 'application/pdf',
            'Connection': 'keep-alive'
        }
    else:
        headers = {
            'Content-Type': 'application/pdf',
            'Connection': 'keep-alive'
        }

    try:
        start = f'{start:02}' # might need to modify accordingly
        response = requests.get(f'{base_url}{start}.pdf', headers=headers, timeout=10)
        response.raise_for_status()

        # successful endpoint response
        if response.status_code == 200 or response.status_code == 201:
            return True
        else:
            print('An error occurred trying to connect to the server')
            return False
        
    except requests.exceptions.RequestException as e:
        print(f'An exception occurred: {e}')
        raise


if __name__ == '__main__':
    load_dotenv()
    try:
        indices = input("Enter start and stop indices to download (inclusive): ")
        start, stop = map(int, indices.split(','))  # Split input by comma and convert to ints
    except ValueError:
        sys.exit("Invalid input. Run the program again!")
    else:
        naming = input("Enter a prefix naming convention: ")
        base_url, cookie = getVars()
        testConnection(base_url, cookie, start)
        recursivePDFDownload(base_url, cookie, naming, start, stop)
