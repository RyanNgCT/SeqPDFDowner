import requests
import os, sys
from dotenv import load_dotenv
import hashlib

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

    status_dict = {}
    success_count, fail_count = 0, 0

    for i in range(start, stop + 1):
        file_index = f'{i:02}' # might need to modify accordingly

        try:
            response = requests.get(f'{base_url}{file_index}.pdf', headers=headers, timeout=timeout_seconds)
            response.raise_for_status()

            file_path = os.path.join(download_dir, f'{naming}{file_index}.pdf')
            with open(file_path, 'wb') as file:
                hasher = hashlib.sha256()
                for chunk in response.iter_content(chunk_size=4096):
                    file.write(chunk)
                    hasher.update(chunk)
                file_hash = hasher.hexdigest()
        except requests.exceptions.RequestException as e:
            print(f'\nFailed to download file {naming}{file_index}.pdf. Error: {e}')
            fail_count += 1
        else:
            line_to_print = f'{naming}{file_index} downloaded successfully. SHA256: {file_hash}'
            print(line_to_print)
            status_dict[i] = line_to_print
            success_count += 1

    with open('out.log', 'w') as f:
        f.write(f'{success_count} files successfully downloaded.\n')
        if fail_count > 0:
            f.write(f'{fail_count} files not downloaded!\n')
        f.write('=================================\n\n')
        for key, val in status_dict.items():
            f.write(f'[{key}] {val}\n')
        f.write('\nOperation Complete.')


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
        
    except Exception as e:
        print(f'An exception occurred: {e}')
        raise

def hashFile(file_path: str):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as file:
        chunk_size = 4096
        while True:
            chunk = file.read(chunk_size)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


if __name__ == '__main__':
    load_dotenv()
    try:
        indices = input("Enter start and stop indices to download (inclusive): ")
        start, stop = map(int, indices.split(','))  # Split input by comma and convert to ints
        if start < 1:
            raise ValueError
    except ValueError:
        sys.exit("Invalid input. Run the program again!")
    else:
        naming = input("Enter a prefix naming convention: ")
        base_url, cookie = getVars()
        testConnection(base_url, cookie, start)
        recursivePDFDownload(base_url, cookie, naming, start, stop)
