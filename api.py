from flask import Flask, jsonify, abort, request
import pandas as pd
import numpy as np

app = Flask(__name__) # package called app that will host the appplication


# The routes are the different URLs that the application implements. In Flask, handlers for the application routes are written as Python functions, called view functions. View functions are mapped to one or more route URLs so that Flask knows what logic to execute when a client requests a given URL.


# sample code for loading the team_info.csv file into a Pandas data frame.  Repeat as
# necessary for other files
def load_teams_data():
    td = pd.read_csv("./team_info.csv")
    return td


def load_table_data(file_addr):
    """Load and return the dataframe from the given csv file."""
    td = pd.read_csv(file_addr)
    return td


# global variables
team_data = load_teams_data()
print("successfully loaded teams data")

game_data = load_table_data("./game.csv")
print("successfully loaded games data")

team_info = load_table_data("./team_info.csv")
print("successfully loaded team info")

game_skater_stats = load_table_data("./game_skater_stats.csv")
print("successfully loaded game skater stats")

game_team_data = load_table_data("./game_teams_stats.csv")
print("successfully loaded game_team_info")

game_plays = load_table_data("./game_plays_2011030221.csv")
print("successfully loaded game plays")

game_plays_players = load_table_data("./game_plays_players_2011030221.csv")
print("successfully loaded game plays players")

player_info = load_table_data("./player_info.csv")
print("successfully loaded player info")


@app.route('/')
def index():
    return "NHL API"


@app.route('/api/teamss/<string:team_id>', methods=['GET'])
def get_s(team_id):
    return "hello"


# route mapping for HTTP GET on /api/schedule/TOR
@app.route('/api/teams/<string:team_id>', methods=['GET'])
def get_task(team_id):
    # fetch sub dataframe for all teams (hopefully 1) where abbreviation=team_id

    teams = team_data[team_data["abbreviation"] == team_id]

    # return 404 if there isn't one team
    if teams.shape[0] < 1:
        abort(404)

    # get first team
    team = teams.iloc[0]

    # return customized JSON structure in lieu of Pandas Dataframe to_json method
    teamJSON = {"abbreviation": team["abbreviation"],
                "city": team["shortName"],
                "name": team["teamName"]}

    # jsonify easly converts maps to JSON strings
    return jsonify(teamJSON)


def merge_games_with_teams(given_games):

    games = given_games.copy()

    home_team = team_info.copy()
    away_team = team_info.copy()

    home_team = home_team.rename(columns={"team_id": "home_team_id",
                                          "franchiseId": "franchiseIdHome",
                                          "shortName": "shortNameHome",
                                          "teamName": "teamNameHome",
                                          "abbreviation": "abbreviationHome",
                                          "link": "linkHome"})

    away_team = away_team.rename(columns={"team_id": "away_team_id",
                                          "franchiseId": "franchiseIdAway",
                                          "shortName": "shortNameAway",
                                          "teamName": "teamNameAway",
                                          "abbreviation": "abbreviationAway",
                                          "link": "linkAway"})

    local_games = games.copy()

    local_games = pd.merge(local_games, home_team, on='home_team_id', how='inner')
    local_games = pd.merge(local_games, away_team, on='away_team_id', how='inner')

    return local_games


@app.route('/api/results', methods=['GET'])
def get_game_data():

    date = request.args.get('date', None)
    games = game_data[game_data["date_time"] == date]

    # return 404 if there isn't one game
    if games.shape[0] < 1:
        abort(404)

    try:
        local_games = merge_games_with_teams(games)

        result = []

        for i in range(local_games.shape[0]):

            cur_game = local_games.iloc[i]

            value0 = cur_game["away_goals"]
            value1 = cur_game["home_goals"]
            value2 = cur_game["home_rink_side_start"]
            value3 = cur_game["outcome"]
            value4 = cur_game["venue"]

            if isinstance(value0, np.integer):
                value0 = int(value0)

            if isinstance(value1, np.integer):
                value1 = int(value1)

            if isinstance(value2, np.integer):
                value2 = int(value2)

            if isinstance(value3, np.integer):
                value3 = int(value3)

            if isinstance(value4, np.integer):
                value4 = int(value4)

            games_json = {
                         "home_team_name": cur_game["teamNameHome"],
                         "away_team_name": cur_game["teamNameAway"],
                         "away_goals": value0,
                         "home_goals": value1,
                         "outcome": value3}
            result.append(games_json)

        return jsonify(result)
    except:
        abort(500)

@app.route('/api/results/<int:ID>/teams', methods=['GET'])
def get_game_results_detailed (ID):

    game_teams = game_team_data[game_team_data["game_id"] == ID]


    # There are was no game found with the given game_id
    if game_teams.shape[0] <1:
        abort(404)

    try:
        team_1 = game_teams.iloc[0]
        team_2 = game_teams.iloc[1]

        print (team_1)
        print (team_2)

        team1_id = int(team_1["team_id"])
        team2_id = int(team_2["team_id"])

        team1_abr = team_data[team_data["team_id"] == team1_id]["abbreviation"].iloc[0]
        team2_abr = team_data[team_data["team_id"] == team2_id]["abbreviation"].iloc[0]

        print (team2_abr)
        print (team1_abr)

        team_1_JSON = {"Team 1" : team1_abr,
                         "Home or Away": team_1["HoA"],
                         "Won": bool(team_1["won"]),
                         "Settled In": team_1["settled_in"],
                         "Goals": int(team_1["goals"]),
                         "Shots": int(team_1["shots"]),
                         "Hits": int(team_1["hits"]),
                         "PIM": int(team_1["pim"]),
                         "PowerPlayOpportunities": int(team_1["powerPlayOpportunities"]),
                         "PowerPlayGoals": int(team_1["powerPlayGoals"]),
                         "FaceOffWinPercentage": float(team_1["faceOffWinPercentage"]),
                         "Giveaways": int(team_1["giveaways"]),
                         "Takeaways": int(team_1["takeaways"])}

        team_2_JSON = {"Team 2": team2_abr,
                       "Home or Away": team_2["HoA"],
                       "Won": bool(team_2["won"]),
                       "Settled In": team_2["settled_in"],
                       "Goals": int(team_2["goals"]),
                       "Shots": int(team_2["shots"]),
                       "Hits": int(team_2["hits"]),
                       "PIM": int(team_2["pim"]),
                       "PowerPlayOpportunities": int(team_2["powerPlayOpportunities"]),
                       "PowerPlayGoals": int(team_2["powerPlayGoals"]),
                       "FaceOffWinPercentage": float(team_2["faceOffWinPercentage"]),
                       "Giveaways": int(team_2["giveaways"]),
                       "Takeaways": int(team_2["takeaways"])}

        game_team1_team2_JSON = [team_1_JSON,team_2_JSON]


        # jsonify easly converts maps to JSON strings
        return jsonify(game_team1_team2_JSON)
    except:
        abort(500)


def merge_games_with_game_skater_stats(given_games):

    games = given_games.copy()
    games = merge_games_with_teams(games)

    game_skaters_home = game_skater_stats.copy()
    game_skaters_away = game_skater_stats.copy()

    game_skaters_home = game_skaters_home.rename(columns={"game_id": "game_id",
                                                          "player_id": "player_id",
                                                          "team_id": "home_team_id",
                                                          "timeOnIce": "timeOnIce",
                                                          "assists": "assists",
                                                          "goals": "goals",
                                                          "shots": "shots",
                                                          "hits": "hits",
                                                          "powerPlayGoals": "powerPlayGoals",
                                                          "powerPlayAssists": "powerPlayAssists",
                                                          "penaltyMinutes": "penaltyMinutes",
                                                          "faceOffWins": "faceOffWins",
                                                          "faceoffTaken": "faceoffTaken",
                                                          "takeaways": "takeaways",
                                                          "giveaways": "giveaways",
                                                          "shortHandedGoals": "shortHandedGoals",
                                                          "shortHandedAssists": "shortHandedAssists",
                                                          "blocked": "blocked",
                                                          "plusMinus": "plusMinus",
                                                          "evenTimeOnIce": "evenTimeOnIce",
                                                          "shortHandedTimeOnIce": "shortHandedTimeOnIce",
                                                          "powerPlayTimeOnIce": "powerPlayTimeOnIce"
                                                          })

    game_skaters_away = game_skaters_away.rename(columns={"game_id": "game_id",
                                                          "player_id": "player_id",
                                                          "team_id": "away_team_id",
                                                          "timeOnIce": "timeOnIce",
                                                          "assists": "assists",
                                                          "goals": "goals",
                                                          "shots": "shots",
                                                          "hits": "hits",
                                                          "powerPlayGoals": "powerPlayGoals",
                                                          "powerPlayAssists": "powerPlayAssists",
                                                          "penaltyMinutes": "penaltyMinutes",
                                                          "faceOffWins": "faceOffWins",
                                                          "faceoffTaken": "faceoffTaken",
                                                          "takeaways": "takeaways",
                                                          "giveaways": "giveaways",
                                                          "shortHandedGoals": "shortHandedGoals",
                                                          "shortHandedAssists": "shortHandedAssists",
                                                          "blocked": "blocked",
                                                          "plusMinus": "plusMinus",
                                                          "evenTimeOnIce": "evenTimeOnIce",
                                                          "shortHandedTimeOnIce": "shortHandedTimeOnIce",
                                                          "powerPlayTimeOnIce": "powerPlayTimeOnIce"
                                                          })

    game_home = pd.merge(games, game_skaters_home, on=['game_id', 'home_team_id'], how='inner')
    game_away = pd.merge(games, game_skaters_away, on=['game_id', 'away_team_id'], how='inner')

    player_info1 = player_info.copy()

    game_home = pd.merge(game_home, player_info1, on=['player_id'], how='inner')
    game_away = pd.merge(game_away, player_info1, on=['player_id'], how='inner')

    return game_home, game_away



def generate_json_for_player_data(game, HoA):

    result = []

    for i in range(game.shape[0]):
        cur_player = game.iloc[i]

        if HoA:
            team_name = cur_player["teamNameHome"]
        else:
            team_name = cur_player["teamNameAway"]

        players_json = {
            "Team": team_name,
            "Player": cur_player["firstName"] + " " + cur_player["lastName"],
            "TimeOnIce": int(cur_player["timeOnIce"]),
            "Assists": int(cur_player["assists"]),
            "Goals": int(cur_player["goals"]),
            "Shots": int(cur_player["shots"]),
            "Hits": int(cur_player["hits"]),
            "PowerPlayGoals": int(cur_player["powerPlayGoals"]),
            "PowerPlayAssists": int(cur_player["powerPlayAssists"]),
            "FaceOffWins": int(cur_player["faceOffWins"]),
            "Takeaways": int(cur_player["takeaways"]),
            "Giveaways": int(cur_player["giveaways"]),
            "ShortHandedGoals": int(cur_player["shortHandedGoals"]),
            "ShortHandedAssists": int(cur_player["shortHandedAssists"]),
            "Blocked": int(cur_player["blocked"]),
            "PlusMinus": int(cur_player["plusMinus"]),
            "EvenTimeOnIce": int(cur_player["evenTimeOnIce"]),
            "ShortHandedTimeOnIce": int(cur_player["shortHandedTimeOnIce"]),
            "PowerPlayTimeOnIce": int(cur_player["powerPlayTimeOnIce"])
        }

        result.append(players_json)

    return result

@app.route('/api/results/<int:game_id>/players', methods=['GET'])
def get_player_stats(game_id):

    games = game_data[game_data["game_id"] == game_id]

    # return 404 if there isn't one game
    if games.shape[0] < 1:
        abort(404)
    try:
        games_home, games_away = merge_games_with_game_skater_stats(games)

        result = generate_json_for_player_data(games_home, True) + generate_json_for_player_data(games_away, False)
        return jsonify(result)
    except:
        abort(500)


def merge_games_with_game_plays(given_game):
    game = given_game.copy()

    game1 = pd.merge(game, game_skater_stats, on=['game_id'], how='inner')
    game2 = pd.merge(game1, player_info, on=['player_id'], how='inner')
    game3 = pd.merge(game2, team_info, on=['team_id'], how='inner')
    game4 = pd.merge(game3, game_plays_players, on=['game_id', 'player_id'], how='inner')
    game5 = pd.merge(game4, game_plays, on=['play_id', 'game_id', 'play_num'], how='inner')

    return game5


class Goal:

    def __init__(self, period_time, cur_game):
        self.period_time = period_time
        self.cur_game = cur_game

    def __ge__(self, other):
        return self.period_time >= other.period_time

    def __le__(self, other):
        return self.period_time <= other.period_time

    def __gt__(self, other):
        return self.period_time > other.period_time

    def __lt__(self, other):
        return self.period_time < other.period_time


def sort_by_goal_time(games):
    periods = {}

    for i in range(games.shape[0]):
        cur_game = games.iloc[i]

        period = cur_game["period"]
        period_time = cur_game["periodTime"]

        g = Goal(period_time, cur_game)
        if period not in periods:
            periods[period] = [g]
        else:
            periods[period].append(g)

    for item in periods.items():
        l = item[1]
        l.sort()
        periods[item[0]] = l

    return periods


def retrieve_name(team_id):
    # retrieve this team's name by its id from team_info table
    team_name = team_data[team_data["team_id"] == team_id]["abbreviation"].iloc[0]
    print (team_name)

    return team_name


def generate_assist_hyperlink(assist_name, game_id):
    games = game_data[game_data["game_id"] == game_id]
    games_and_skaters = pd.merge(games.copy(), game_skater_stats.copy(), on=['game_id'], how='inner')
    games_players_info = pd.merge(games_and_skaters.copy(), player_info.copy(), on=['player_id'],
                                  how='inner')

    games_and_players = games_players_info[games_players_info["firstName"] == assist_name.split(' ')[0]]
    games_and_players = games_players_info[games_players_info["lastName"] == assist_name.split(' ')[1]]

    return "http://127.0.0.1:5000/api/results/players/" + str(int(games_and_players["player_id"]))


def extract_name(str_with_name):
    str_arr = str_with_name.split(' ')
    return str_arr[0] + " " + str_arr[1]


def parse_assists(game_id, assists):

    result = []
    finished = False

    while ', ' in assists or not finished:

        if ', ' in assists:
            str_arr = assists.split(', ')
            name = extract_name(str_arr[0])
            result.append(str_arr[0] + " " + generate_assist_hyperlink(name, game_id))
            assists = str_arr[1]
        else:
            name = extract_name(assists)
            result.append(assists + " " + generate_assist_hyperlink(name, game_id))
            finished = True


    result_str = ""
    for i in range(len(result)):
        result_str += result[i]
        if i != len(result) - 1:
            result_str += ", "
    return result_str


@app.route('/api/results/<int:game_id>/scoringsummary', methods=['GET'])
def get_scoring_summary(game_id):
    games = game_data[game_data["game_id"] == game_id]

    # return 404 if there isn't one game
    if games.shape[0] < 1:
        abort(404)
    try:
        games_with_plays = merge_games_with_game_plays(games)

        sorted_goals = sort_by_goal_time(games_with_plays)

        result = []
        items = [(k, v) for k, v in sorted_goals.items()]

        prev_periodTime = 0
        for i in range(len(items)):
            goals = items[i][1]

            for j in range(len(goals)):
                cur_game = goals[j].cur_game

                team_name_home = retrieve_name(int(cur_game["home_team_id"]))
                team_name_away = retrieve_name(int(cur_game["away_team_id"]))

                if cur_game["event"] == "Goal":
                    if (int(goals[j].period_time) != prev_periodTime):
                        prev_periodTime = int(goals[j].period_time)

                        assists_string = ""

                        assists_string = cur_game["description"].split("assists: ")[1]
                        unassisted = True

                        assists_check = cur_game["description"].split("assists:")[1]
                        if len(assists_check) != 0:
                            assists_string = parse_assists(cur_game["game_id"], assists_string)
                            unassisted = False

                        json = {}

                        if not unassisted:
                            json = {
                                "player": cur_game["firstName"] + " " + cur_game["lastName"] + " " + "http://127.0.0.1:5000/api/results/players/" + str(cur_game["player_id"]),
                                "assists": assists_string,
                                "period": int(items[i][0]),
                                "periodTime": str(int(goals[j].period_time/60)) + ":" + str('%02d' % int(goals[j].period_time%60)),
                                team_name_home: int(cur_game["goals_home"]),
                                team_name_away: int(cur_game["goals_away"])
                            }
                        else:
                            json = {
                                "player": cur_game["firstName"] + " " + cur_game["lastName"] + " " + "http://127.0.0.1:5000/api/results/players/" + str(cur_game["player_id"]),
                                "assists": "unassisted",
                                "period": int(items[i][0]),
                                "periodTime": str(int(goals[j].period_time/60)) + ":" + str('%02d' % int(goals[j].period_time%60)),
                                team_name_home: int(cur_game["goals_home"]),
                                team_name_away: int(cur_game["goals_away"])
                            }
                        result.append(json)

        return jsonify(result)
    except:
        abort(500)


if __name__ == '__main__':
    app.run(debug=True)
