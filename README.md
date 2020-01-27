# Assignment 1

# User stories
1) As a hockey fan, I want data about games on a given date, so that I can quickly get to know about what games will be happening on that day.

2) As a stat junkie, I want detailed results about games, so I can keep track of how each team is performing.

3) As a fantasy hockey player, I want data about performance of individual players, so that I can assess their performance based on various measures.

# Acceptance criteria
First:
* Ability to specify the date to provide schedule for.

* For each game that happened on the given date, provide: away team name, home team name, away goals, home goals, outcome.

Second:
* Ability to provide game id.

* For each game, provide stats for each team: If they are home or away, If team won in regular or overtime, number of goals, number of shots, number of hits, number of penalty minutes, number of power play goals,
number of power play opportunities, faceoff win percentage, number of giveaways, number of takeaways.

Third:
* Ability to provide game id.

* For each player in each team of the game with the given game id, provide: assists, blocked, even time on ice, face off wins, giveaways, goals, hits, full name, plus minus, power play assists, power play goals, power play time on ice, short-handed assists, short-handed goals, short-handed time on ice, shots, takeaways, team name, time on ice.   

# Game Results Summary

URL: /api/results?date=YYYY-MM-DD, example: /api/results?date=2011-05-20

Design Overview: Given a request, we first need to extract the date from request arguments. Then we load the data from game.csv file into a dataframe. Next we obtain a dataframe for games that happened on the given date. After that, we load team_info.csv into a dataframe and produce two copies of it. We rename columns in both team dataframes by prefixing some of them with home_ or away_ in order to avoid naming collisions when merging them later. After that, we merge our games dataframe with each of two team dataframes. By following this procedure, we obtain all the information about the game and also names of the teams. After that, we iterate through rows of our dataframe, extract needed information from columns and insert it into dictionary. We then pass this collection of  dictionaries to jsonify and return its return value.

JSON Structure: home_team_name, away_team_name, home_goals, away_goals, outcome


# Game Results Details

URL: /api/results/{ID}/teams, where ID is a unique game ID

Design Overview: Given a game_ID, it is then indexed into game_team_stats csv file with game_id. Doing this provides all the information needed for this task, except the team name abbervation.
To get the abbervation, we indexed the team_id for both teams in the team_info csv file. Then provided all the needed information into lists, to then be sent to JSONIFY.

JSON Structure: The data structure is seperated into team 1 and team 2.
For each team the JSON data provided is: team_name, home or away, won, settled in, goals, shots, hits, pim, powerplayOppurtunities, powerplayGoals, faceoff win percentage, giveaways, takeaways
Then after JSON data for each team is created. They are combined and made into JSON format.


# Game Player Stats

URL: /api/results/{ID}/players, where ID is a unique game ID

Design Overview: First we load data from games.csv file into a dataframe. Then we use the given game_id to obtain dataframe where all entries have given value as their game id. After that we load game_skater_stats.csv and player_info.csv into dataframes. and make two copies of them. We rename their columns to avoid naming collisions when merging. Then we merge each of them with games and player_info dataframes to obtain two dataframes that contain detailed information for each player in home and away teams. After that we iterate through rows these data frames and extract data into dictionaries. After that, we call jsonify on collection of these dictionaries and return its return value.

JSON Structure: For a given game_ID, our merged database is itterated through to get all the players on both teams to provide for each player:
Team, Player Name, TimeOnIce, Assists, Goals, Shots, Hits, PowerPlayGoals, PowerPlayAssists, FaceOffWins, Takeaways, Giveaways, ShortHandedGoals, ShortHandedAssists, Blocked, PlusMinus, EvenTimeOnIce, ShortHandedTimeOnIce, PowerPlayTimeOnIce
This data is looped through for each player on both teams and then appended and JSONIFY'd.


# Enhancements, Game Scoring Timeline

URL: /api/results/{ID}/scoringsummary, where ID is a unique game ID

Design Overview: We first load games.csv into a dataframe. Using given game_id, we obtain a dataframe that only contains entries that have same game ids as the one provided. After that we load game_plays and game_plays_players csv files into dataframes. After that we merge our dataframe for games with dataframes for game_plays, game_plays_players, game_skater_stats, player_info, team_info, we load prior to merging. After that we iterate through rows of this combined dataframes and create instances of class Goal from them. After that, we use built-in sorting algorithm of list in order to sort the goals by period and period time. After that, we extract all the data from goals into dictionaries. Next, we pass this collection of dictionaries to jsonify and return its return value.

JSON Structure: For a given game_id, by itterating through our merged database and selecting only the event that is only "goal" the info provided is:
Player who scored, assists for the goal, period, period time, and the score at that time.
For the player who scored, and the assits there is hyperlink that is provided for player data for that player.

# Setup and running

Setup: 
1) you will need to install Python 3.7.4
Detailed instructions on how this can be done can be found here: https://www.python.org/downloads/
2) you will need to install pandas. Instructions on how this can be done can be found here:  https://pandas.pydata.org/pandas-docs/stable/install.html
3) you will need to install flask. Instructions on how this can be done can be found here: https://flask.palletsprojects.com/en/1.1.x/installation/

Project: 

This project can be cloned to your machine using Git. Instruction on how to use Git: https://product.hubspot.com/blog/git-and-github-tutorial-for-beginners

Running: 

1. Navigate to the project folder you have just cloned using terminal/console. Instructions for 

    Mac: https://macpaw.com/how-to/use-terminal-on-mac, 

    Linux: https://www.howtogeek.com/140679/beginner-geek-how-to-start-using-the-linux-terminal/, 
    
    Windows: https://gist.github.com/jirutka/99d57c82fa8981f56fb5
    
2. After that, type:

        python api.py 
        
and press Enter

# Test Cases:
Make sure that you are running this application on the port 5000. Otherwise you may need to change 5000 to the port number that you are using in every URL provided below.


We provide a test case for each question: 

Game Results Summary Test: 
http://127.0.0.1:5000/api/results?date=2011-05-01


Game Result Details Test: http://127.0.0.1:5000/api/results/2011030223/teams


Game Player Stats Test: http://127.0.0.1:5000/api/results/2011030223/players


Enhancements Test: http://127.0.0.1:5000/api/results/2011030221/scoringsummary


