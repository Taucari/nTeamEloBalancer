# nTeamEloBalancer
Finding the most balanced teams based on player elo.

## Requirements
Check requirements.txt

As of 2022-8-2, only pprint is needed and only for nicely printing the dictionaries.

## Usage
1. Enter in the player names and their elos into config.py
2. Set the team size
3. Run main.py

### Extra Settings
| Setting | Description |
| --- | --- |
| DECIMAL_PLACES | Number of decimal places to round to |
| PRINT_ALL_COMBINATIONS | Use pprint to show all possible combinations of teams |
| PRINT_BEST_COMBINATION | Use pprint to show best combination of teams where the standard deviation between teams is lowest |
