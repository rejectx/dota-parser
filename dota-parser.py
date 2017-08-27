import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function that returns team_name and team_url of teams listed on Liquidpedia.
def get_teams_url_list():
    data = {}
    page = requests.get('http://wiki.teamliquid.net/dota2/Portal:Teams')
    soup = BeautifulSoup(page.content, 'html.parser')
    # Parsing only currently active teams from 4 regions, [0:8] slice would make it to retrieve former teams also.
    regions = soup.find_all('div', {'class' : 'template-box'})[0:4]
    for region in regions:
        teams = region.find_all('span', {'class' : 'team-template-text'})
        for team in teams:
            data[team.get_text()] = team.find('a').get('href')
    return data

def parse_team_page(team_url):
    page = requests.get(team_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    players = soup.find('div', {'class' : 'activesquad'})
    players = players.find_all('tr')
    #player = players[2].find_all('td')
    for player in players[2:]:
        player = player.find_all('td')
        nation = player[0].find('a').get('title')
        nickname = player[1].find('a').get('title')
        player_url = player[1].find('a').get('href')
        fullname = player[2].get_text().strip()
        position = player[3].get_text()
        print(nation, nickname, player_url, fullname, position)


# Code that is executed on the start.
def main():
    # parse_team_page('http://wiki.teamliquid.net/dota2/OG')
    teams = get_teams_url_list()
    for key, value in teams.items():
        print(key)
        parse_team_page('http://wiki.teamliquid.net'+value)



# Standard boiler plate for main() function.
if __name__ == '__main__':
    main()
