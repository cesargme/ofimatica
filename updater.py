import requests
import zipfile
import shutil
import os

def get_latest_version():
    response = requests.get('https://api.github.com/repos/cesargme/ofimatica/tags')
    response.raise_for_status()
    tags = response.json()
    if not tags:
        return None
    return tags[0]['name']

def download_and_extract_zip(url, extract_to='.'):
    response = requests.get(url)
    response.raise_for_status()
    with open('temp.zip', 'wb') as f:
        f.write(response.content)
    with zipfile.ZipFile('temp.zip', 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    os.remove('temp.zip')

def update_program():
    latest_version = get_latest_version()
    if latest_version != CURRENT_VERSION:
        print('Updating to version', latest_version)
        url = 'https://github.com/cesargme/ofimatica/archive/refs/tags/' + latest_version + '.zip'
        download_and_extract_zip(url)
        print('Update complete')

def get_current_version():
    with open('version.txt', 'r') as f:
        return f.read().strip()