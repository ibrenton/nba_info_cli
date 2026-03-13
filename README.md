# NBA Stats Tool

A Python tool for fetching real-time NBA game statistics, scores, and schedules using the ESPN API.

## 🎮 Two Ways to Use

### 1. Interactive UI (Recommended for most users)
Launch the user-friendly menu interface:
```bash
python3 start.py
```
Or:
```bash
python3 nba_ui.py
```

See **[UI_GUIDE.md](UI_GUIDE.md)** for complete UI documentation.

### 2. Python API (For developers)
Use the Python module in your own scripts:
```python
from nba_stats import NBAStats
nba = NBAStats()
games = nba.get_recent_games(days=7)
```

See the API Reference section below for details.

## Features

- ✅ **Interactive User Interface** - Easy-to-use menu system
- ✅ **Recent Game Scores** - Get scores from completed games over the past N days
- ✅ **Upcoming Game Schedules** - View scheduled games for the next N days
- ✅ **Detailed Game Statistics** - Retrieve player-by-player stats for specific games
- ✅ **Team Filtering** - Filter results by specific teams
- ✅ **Team Information** - Get list of all NBA teams
- ✅ **Win/Loss Tracking** - Automatic record calculation for teams
- ✅ **No API Key Required** - Uses ESPN's public API

## Installation

1. Clone or download this repository
2. Install required dependencies:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install requests
```

## Quick Start

### Basic Usage

```python
from nba_stats import NBAStats

# Initialize the client
nba = NBAStats()

# Get recent games from the last 7 days
recent_games = nba.get_recent_games(days=7)
nba.display_recent_games(recent_games)

# Get upcoming games for the next 7 days
upcoming_games = nba.get_upcoming_games(days=7)
nba.display_upcoming_games(upcoming_games)

# Get detailed stats for a specific game
game_stats = nba.get_game_stats(game_id='401704980')
nba.display_game_stats(game_stats)
```

## CLI Examples

Run quick commands from the terminal without entering the interactive UI:

```bash
# Show recent games from the last 3 days
python3 start.py --recent 3

# Show upcoming games for the next 5 days for the Lakers
python3 start.py --upcoming 5 --team LAL

# Get detailed stats for a specific game ID
python3 start.py --stats 401704980

# List all teams
python3 start.py --teams

# Run the interactive menu
python3 start.py --interactive
```

### Filter by Team

```python
# Get recent Lakers games
lakers_games = nba.get_recent_games(days=7, team='LAL')

# Get upcoming Warriors games
warriors_upcoming = nba.get_upcoming_games(days=7, team='GSW')
```

### Get All Teams

```python
teams = nba.get_teams()
for team in teams:
    print(f"{team['abbreviation']} - {team['displayName']}")
```

## API Reference

### `NBAStats()`

Main class for interacting with NBA data.

#### Methods

##### `get_recent_games(days=7, team=None)`

Get recent game scores from completed games.

**Parameters:**
- `days` (int): Number of days to look back (default: 7)
- `team` (str, optional): Team abbreviation to filter by (e.g., 'LAL', 'BOS')

**Returns:** List of game dictionaries containing:
- `id`: Game ID
- `date`: Game date/time
- `status`: Game status (e.g., "Final")
- `home_team`: Home team name
- `home_team_abbr`: Home team abbreviation
- `home_score`: Home team score
- `visitor_team`: Visiting team name
- `visitor_team_abbr`: Visiting team abbreviation
- `visitor_score`: Visiting team score
- `season`: Season year
- `venue`: Venue name

**Example:**
```python
games = nba.get_recent_games(days=3, team='LAL')
for game in games:
    print(f"{game['visitor_team_abbr']} {game['visitor_score']} @ "
          f"{game['home_team_abbr']} {game['home_score']}")
```

##### `get_upcoming_games(days=7, team=None)`

Get scheduled games for upcoming days.

**Parameters:**
- `days` (int): Number of days to look ahead (default: 7)
- `team` (str, optional): Team abbreviation to filter by

**Returns:** List of scheduled game dictionaries (similar structure to recent games, but without scores)

**Example:**
```python
upcoming = nba.get_upcoming_games(days=5, team='GSW')
for game in upcoming:
    print(f"{game['date'][:10]}: {game['visitor_team_abbr']} @ {game['home_team_abbr']}")
```

##### `get_game_stats(game_id)`

Get detailed player statistics for a specific game.

**Parameters:**
- `game_id` (str): The unique game ID

**Returns:** Dictionary containing:
- `game_id`: Game ID
- `date`: Game date
- `home_team`: Home team name
- `home_score`: Home team score
- `visitor_team`: Visiting team name
- `visitor_score`: Visiting team score
- `home_player_stats`: List of home player statistics
- `visitor_player_stats`: List of visitor player statistics

Each player stat includes:
- `player`: Player name
- `team`: Team abbreviation
- `minutes`: Minutes played
- `points`: Points scored
- `rebounds`: Total rebounds
- `assists`: Assists
- `steals`: Steals
- `blocks`: Blocks
- `turnovers`: Turnovers
- `fg`: Field goals (made-attempted)
- `fg3`: Three-pointers (made-attempted)
- `ft`: Free throws (made-attempted)

**Example:**
```python
stats = nba.get_game_stats('401704980')
print(f"{stats['visitor_team']} {stats['visitor_score']} @ "
      f"{stats['home_team']} {stats['home_score']}")

for player in stats['home_player_stats']:
    print(f"{player['player']}: {player['points']} pts, "
          f"{player['rebounds']} reb, {player['assists']} ast")
```

##### `get_teams()`

Get list of all NBA teams.

**Returns:** List of team dictionaries containing:
- `id`: Team ID
- `abbreviation`: Team abbreviation
- `displayName`: Full team name
- `location`: Team location
- `name`: Team name
- `logo`: Team logo URL

##### Display Methods

- `display_recent_games(games)`: Pretty print recent games
- `display_upcoming_games(games)`: Pretty print upcoming games
- `display_game_stats(stats)`: Pretty print game statistics

## Common Team Abbreviations

| Abbreviation | Team |
|-------------|------|
| ATL | Atlanta Hawks |
| BOS | Boston Celtics |
| BKN | Brooklyn Nets |
| CHA | Charlotte Hornets |
| CHI | Chicago Bulls |
| CLE | Cleveland Cavaliers |
| DAL | Dallas Mavericks |
| DEN | Denver Nuggets |
| DET | Detroit Pistons |
| GSW | Golden State Warriors |
| HOU | Houston Rockets |
| IND | Indiana Pacers |
| LAC | LA Clippers |
| LAL | Los Angeles Lakers |
| MEM | Memphis Grizzlies |
| MIA | Miami Heat |
| MIL | Milwaukee Bucks |
| MIN | Minnesota Timberwolves |
| NO | New Orleans Pelicans |
| NY | New York Knicks |
| OKC | Oklahoma City Thunder |
| ORL | Orlando Magic |
| PHI | Philadelphia 76ers |
| PHX | Phoenix Suns |
| POR | Portland Trail Blazers |
| SAC | Sacramento Kings |
| SA | San Antonio Spurs |
| TOR | Toronto Raptors |
| UTAH | Utah Jazz |
| WSH | Washington Wizards |

## Running the Application

### Interactive UI (Recommended)

Launch the interactive menu interface:

```bash
python3 start.py
```

This gives you an easy-to-use menu system where you can:
- Browse recent and upcoming games
- Search by team
- View detailed statistics
- See team records

See **[UI_GUIDE.md](UI_GUIDE.md)** for complete UI instructions.

### Demo Scripts

Run the included demo scripts to see all features in action:

```bash
python3 demo.py      # Comprehensive demo
python3 examples.py  # Practical examples
python3 nba_stats.py # Basic demo
```

## Examples

### Track Your Favorite Team

```python
from nba_stats import NBAStats

nba = NBAStats()
team = 'LAL'  # Lakers

print(f"{team} Recent Performance:")
recent = nba.get_recent_games(days=10, team=team)
for game in recent:
    if game['home_team_abbr'] == team:
        result = "W" if game['home_score'] > game['visitor_score'] else "L"
        print(f"{result}: vs {game['visitor_team_abbr']} ({game['home_score']}-{game['visitor_score']})")
    else:
        result = "W" if game['visitor_score'] > game['home_score'] else "L"
        print(f"{result}: @ {game['home_team_abbr']} ({game['visitor_score']}-{game['home_score']})")

print(f"\n{team} Upcoming Schedule:")
upcoming = nba.get_upcoming_games(days=7, team=team)
for game in upcoming:
    opponent = game['home_team_abbr'] if game['visitor_team_abbr'] == team else game['visitor_team_abbr']
    location = "@" if game['visitor_team_abbr'] == team else "vs"
    print(f"{game['date'][:10]}: {location} {opponent}")
```

### Get Today's Scores

```python
from nba_stats import NBAStats

nba = NBAStats()
today_games = nba.get_recent_games(days=1)

print("Today's NBA Scores:")
for game in today_games:
    print(f"{game['visitor_team_abbr']} {game['visitor_score']} @ "
          f"{game['home_team_abbr']} {game['home_score']} - {game['status']}")
```

### Find Top Performers in a Game

```python
from nba_stats import NBAStats

nba = NBAStats()
recent = nba.get_recent_games(days=1)

if recent:
    game_id = recent[0]['id']
    stats = nba.get_game_stats(game_id)
    
    all_players = stats['home_player_stats'] + stats['visitor_player_stats']
    # Sort by points
    all_players.sort(key=lambda x: int(x.get('points', 0)), reverse=True)
    
    print("Top 5 Scorers:")
    for i, player in enumerate(all_players[:5], 1):
        print(f"{i}. {player['player']} ({player['team']}): {player['points']} pts")
```

## Data Source

This tool uses the ESPN API for NBA data. No API key is required.

## Requirements

- Python 3.6+
- requests library

## License

This tool is provided as-is for educational and personal use.

## Contributing

Feel free to submit issues or pull requests to improve this tool!

## Notes

- Game IDs can be obtained from the `get_recent_games()` or `get_upcoming_games()` methods
- All times are in UTC
- The tool fetches real-time data, so scores and schedules are always current
- During the off-season, game data may be limited

## Troubleshooting

**No games found:**
- Check if there are NBA games scheduled for the date range
- The NBA season typically runs from October to June
- Verify your internet connection

**SSL Warnings:**
- These are harmless warnings about SSL library versions and can be ignored
- They don't affect the functionality of the tool

**API Errors:**
- If you receive errors, the ESPN API may be temporarily unavailable
- Wait a few moments and try again
