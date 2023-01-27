from bs4 import BeautifulSoup
import requests
import pandas as pd


def get_teams(url):
    team_data, team_urls = [], []

    s = requests.Session()
    response = s.get(url, timeout=10)

    soup = BeautifulSoup(response.content, "html.parser")
    right_table = soup.find("table", {"class": "wikitable sortable"})

    rows = right_table.findAll("tr")

    for row in rows[1:]:
        data = []
        for index, cell in enumerate(row.select("td")[:-2]):
            data.append(cell.text.rstrip())
            if index == 0:
                print(cell)
                team_urls.append(cell.a["href"])
        team_data.append(data)

    return team_data, team_urls


def get_team_data(team_url, team_data):
    pass


def main():
    wiki_url = "https://en.wikipedia.org"
    league_url = "https://en.wikipedia.org/wiki/2022%E2%80%9323_Bundesliga"
    team_data, team_urls = get_teams(league_url)

    for index, team in enumerate(team_urls):
        team_url = wiki_url + team
        print(team_url, team_data[index])
        get_team_data(team_url, team_data[index])


main()
