# nTeamEloBalancer
Finding the most balanced teams based on player elo.

## Requirements
Check requirements.txt

As of 2022-8-2, only pprint is needed and only for nicely printing the dictionaries.

## Usage
1. Enter in the player names and their elos into config.py

      For each player, list their Elo or Elos as shown:
      ```
      PLAYER_LIST = {'Player1': [2069, 2067],
                     'Player2': [1409, 1407],
                     'Player3': [1873, 1871],
                     'Player4': [918],
                     'Player5': [1363],
                     'Player6': [2021],
                     }
      ```
      It does not matter how many Elos you put in or if there are different numbers of Elos for different players. For each player the mean of the Elos will be taken.

      The only restriction is that every player name has to be unique and the number of players has to be a multiple of TEAM_SIZE

2. Set the team size
3. Run main.py

### Extra Settings
| Setting | Description |
| --- | --- |
| DECIMAL_PLACES | Number of decimal places to round to |
| PRINT_ALL_COMBINATIONS | Use pprint to show all possible combinations of teams |
| PRINT_BEST_COMBINATION | Use pprint to show best combination of teams where the standard deviation between teams is lowest |
