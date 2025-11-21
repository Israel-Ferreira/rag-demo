import requests

def download_csv(url, filename):
    response = requests.get(url)

    response.raise_for_status()

    filepath = f"./data/{filename}"

    with open(filepath, "wb") as f:
        f.write(response.content)

