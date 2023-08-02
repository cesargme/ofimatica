import requests
import zipfile
import shutil
import os
import subprocess

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
        # Extract all files into a temporary directory
        temp_dir = 'temp_dir'
        zip_ref.extractall(temp_dir)
    os.remove('temp.zip')

    # Get the name of the top-level directory in the zip file
    # This is based on the assumption that the zip file contains one top-level directory with the name 'ofimatica-0.1'
    dir_name = os.listdir(temp_dir)[0]

    # Copy all files from the top-level directory to the current directory
    source_dir = os.path.join(temp_dir, dir_name)
    target_dir = extract_to
    for file_name in os.listdir(source_dir):
        target_file_path = os.path.join(target_dir, file_name)
        if os.path.exists(target_file_path):
            os.remove(target_file_path)
        shutil.move(os.path.join(source_dir, file_name), target_dir)


    # Delete the temporary directory
    shutil.rmtree(temp_dir)


def update_program(latest_version):
    print('Updating to version', latest_version)

    # Get the name of the current branch
    current_branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD']).decode().strip()

    # Stash any local changes so they don't interfere with the pull
    subprocess.check_call(['git', 'stash'])

    # Pull the latest code
    subprocess.check_call(['git', 'pull', 'origin', current_branch])

    # Update the version file
    with open('version.txt', 'w') as f:
        f.write(latest_version)

    print('Update complete')
    
    # url = 'https://github.com/cesargme/ofimatica/archive/refs/tags/' + latest_version + '.zip'
    # download_and_extract_zip(url)
    # print('Update complete')

def get_current_version():
    if not os.path.exists('version.txt'):
        with open('version.txt', 'w') as f:
            f.write(get_latest_version())
    with open('version.txt', 'r') as f:
        return f.read().strip()
