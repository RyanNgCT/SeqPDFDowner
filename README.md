# SeqPDFDowner

A sequential pdf downloader script I built when I was lazy to manually click and download pdfs by scrolling and clicking through tabs.

## Setup:
1. Clone this repo
```
$ git clone https://github.com/RyanNgCT/SeqPDFDowner.git
```

2. Install requirements
```bash
$ pip install -r requirements.txt
```

3. Configure your `BASE_URL` and copy your user `COOKIE` into a `.env` file.

A base url would look something like: `https://download[.]me/example-`, given pdfs to download like:
```
https://download[.]me/example-01[.]pdf
https://download[.]me/example-02[.]pdf
...
https://download[.]me/example-100[.]pdf
```

So the final config should be like this:

```python
BASE_URL = 'https://download[.]me/example-'
COOKIE = '<replace with your cookie here>'
```

## Disclaimer
I am not liable for any misuse of my software and don't provide any warranty for them.