from bs4 import BeautifulSoup
import requests

month = input("Enter month (01-12): ")
day = input("Enter day (01-31): ")
year = input("Enter year (2021-2022): ")
game_date = year + "-" + month + "-" + day
print()

full_schedule_url = "https://www.basketball-reference.com/teams/LAL/2022_games.html"
full_schedule = requests.get(full_schedule_url)
full_schedule_doc = BeautifulSoup(full_schedule.text, "html.parser")

schedule_table = full_schedule_doc.find_all('tbody')[0]
table_rows = schedule_table.find_all('tr')
game_row = None
for row in table_rows:
    data_cell = row.td
    if (data_cell != None):
        if (data_cell["csk"] == game_date):
            game_row = row
hyperlink = game_row.find_all('a')[1]
box_score_url = f"https://www.basketball-reference.com/{hyperlink['href']}"

box_score = requests.get(box_score_url)
box_score_doc = BeautifulSoup(box_score.text, "html.parser")

title_tag = box_score_doc.title.string
title_contents = title_tag.split()

both_teams = ""
for word in title_contents:
    if (word == "Box"):
        break
    both_teams += word + " "
both_teams = both_teams.replace("at", "@")

meta_tag = box_score_doc.find_all('meta')[3]
meta_contents = meta_tag["content"].split()
final_score = ""
for word in meta_contents:
    if ("(" in word):
        final_score += word

dash_added = False
for char in final_score:
    if (char == ")"):
        if (dash_added == False):
            final_score = final_score.replace(")", " - ", 1)
            dash_added = True
final_score = final_score.replace(")", "")
final_score = final_score.replace("(", "")

player_tr_tags = []
Lakers_table = box_score_doc.find('table', {"id": "box-LAL-game-basic"})
Lakers_table_rows = Lakers_table.find_all('tr')
for row in Lakers_table_rows:
    th_tag = row.th
    if (th_tag.a != None):
        player_tr_tags.append(row)

team_data = []
for tag in player_tr_tags:
    player_name = tag.a.contents[0]
    tov_tag = tag.find("td", {"data-stat": 'tov'})
    if (tov_tag != None):
        player_tov = tov_tag.contents[0]
        team_data.append((player_name, player_tov))

team_data.sort(key=lambda i: i[1], reverse=True)

final_score_label = "       ⚪ Final Score: "
print("⚪", both_teams, "⚪")
print(final_score_label, final_score, "⚪")
print("           Name           Turnovers")
print("           ----           ---------")

for player in team_data:
    indentation = "        "
    player_name = player[0].ljust(19, " ")
    print(indentation, player_name, " - ", player[1])

