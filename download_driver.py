import argparse
import os
import requests
import zipfile


args = argparse.ArgumentParser(add_help="Download latest chrome driver")
options = args.parse_args()


def get_chrome_latest_release():
    url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
    response = requests.request("GET", url)
    return response.text

def write_response_stream(filename, response):
    with open(filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            # Filter out to keep alive-new chunks
            if chunk:
                f.write(chunk)

def download_latest_chrome():
    latest_ver = get_chrome_latest_release()
    url = f"https://chromedriver.storage.googleapis.com/{latest_ver}/chromedriver_win32.zip"
    zip_filename = url.split("/")[-1]
    response = requests.get(url, stream=True)  # Stream allow for immediate download
    write_response_stream(zip_filename, response)
    return zip_filename

def extract_one(zip_filename, target_filename):
    with zipfile.ZipFile(zip_filename) as zip_file:
        zip_file.extract(target_filename)


def main():
    zip_filename = download_latest_chrome()
    extract_one(zip_filename, "chromedriver.exe")
    os.remove(zip_filename)


if __name__ == "__main__":
    main()