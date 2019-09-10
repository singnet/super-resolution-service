#!/usr/bin/env python3

import argparse
import requests
import pathlib

parser = argparse.ArgumentParser(description="Download model/weights for the service.")
parser.add_argument('--filepath',
                    type=str,
                    help="Specifies the full path of the model (including its name).")
# Example: default="/opt/singnet/semantic-segmentation-aerial/service/models/segnet_final_reference.pth"

parser.add_argument('--google_file_id',
                    type=str,
                    help="The ID of the Google Drive file to be downloaded.")
# Example: default="1cwXe8ANkhFqe2i_UNxpZu15y2HZ0N9KN"


def download_file_from_google_drive(file_id, destination):
    def get_confirm_token(server_response):
        for key, value in server_response.cookies.items():
            if key.startswith('download_warning'):
                return value

        return None

    def save_response_content(server_response, file_destination):
        chunk_size = 32768

        with open(file_destination, "wb") as f:
            for chunk in server_response.iter_content(chunk_size):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

    url = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(url, params={'id': file_id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': file_id, 'confirm': token}
        response = session.get(url, params=params, stream=True)

    save_response_content(response, destination)


if __name__ == "__main__":
    args = parser.parse_args()

    # Creates the directory using pathlib
    path = pathlib.Path(args.filepath)
    path.parent.mkdir(parents=True, exist_ok=True)

    # Downloads the google drive file
    try:
        download_file_from_google_drive(args.google_file_id, args.filepath)
        exit(0)
    except Exception as e:
        print(e)
        exit(1)
