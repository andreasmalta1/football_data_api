import requests
import os
from login import login


def post_logos():
    logos_url = "https://thefootballdata.com/api/images/teams"

    access_token = login()
    post_headers = {"Authorization": "Bearer " + access_token}

    logos_dir = r"C:\Users\andreas\Documents\Projects\football_data_api\post_data\logos_to_upload"
    list_logos = os.listdir(logos_dir)

    for logo in list_logos:
        logo_id = logo.split(".")[0]
        url = f"{logos_url}/{logo_id}"
        path = os.path.join(logos_dir, logo)
        files = [("file", (logo, open(path, "rb"), "image/png"))]

        response = requests.post(url, headers=post_headers, files=files)

        print(files)
        print(response)


post_logos()
