import requests
import gspread
from login import login


def post_teams():
    sa = gspread.service_account(filename="service_account.json")
    sh = sa.open("Football Api")
    whs = sh.worksheet("Sheet1")
    values = whs.get_all_values()
    header_column = values[0]
    values.pop(0)

    access_token = login()
    post_headers = {"Authorization": "Bearer " + access_token}

    post_url = "https://thefootballdata.com/api/teams/"

    for row in values:
        post_payload = {}
        for index, column in enumerate(row):
            post_payload[header_column[index]] = column
        response = requests.post(post_url, headers=post_headers, json=post_payload)

        print(response)


post_teams()
